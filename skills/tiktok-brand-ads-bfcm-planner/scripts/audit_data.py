#!/usr/bin/env python3
"""Audit complete bundled CSV release without network/account access."""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
import benchmark as b


def audit():
    cfg=b.config(); errors=[]; tables={}; report={}
    def check(ok, message):
        if not ok: errors.append(message)
    for sheet in cfg['sheets']:
        path=b.ROOT/'references'/sheet['file'];raw=path.read_bytes()
        check(hashlib.sha256(raw).hexdigest()==sheet['sha256'],path.name+': checksum mismatch')
        rows=b.csv_rows(raw.decode('utf-8-sig'))
        nonempty=[(i,r) for i,r in enumerate(rows,1) if any(c.strip() for c in r)]
        report[sheet['purpose']]={'file':path.name,'sha256':hashlib.sha256(raw).hexdigest(),'physical_rows':len(rows),'nonempty_rows':len(nonempty)}
        if sheet['purpose']=='calendar_and_tiers':
            calendar={b.norm(row[0]):(i,row) for i,row in nonempty}
            for phase in cfg['phases']:
                _,row=calendar[b.norm(phase['name'])]
                for index,year in [(1,2026),(2,2025)]:
                    expected='-'.join(phase[k+'_'+str(year)][5:].replace('-','') for k in ['start','end'])
                    check(row[index]==expected,f'Calendar mismatch: {phase["name"]}/{year}')
            check(calendar['baseline (bau)'][1][1]=='0901-0930','BAU mismatch')
            for tier,val in [('t1','≥5000'),('t2','1000-5000'),('t3','0-1000')]:
                check(calendar[tier][1][1]==val,'Tier reference mismatch: '+tier)
            continue
        if sheet['purpose'].endswith('_country_mapping'):
            header,data=b.country_rows(rows, sheet['purpose'].split('_')[0])
        else:
            header=rows[0]; nh=[b.norm(h) for h in header]
            check(len(set(nh))==len(nh) and all(nh),path.name+': blank/duplicate header')
            data=[]
            for i,row in nonempty[1:]:
                check(len(row)==len(header),f'{path.name}:{i} row width')
                data.append((i,dict(zip(header,row))))
        tables[sheet['purpose']]=data
        keys=b.KEYS+(['Phase Order'] if sheet['purpose']=='creative' else [])
        mapping=sheet['purpose'].endswith('_country_mapping')
        if mapping:keys=[header[0]]
        seen=Counter(tuple(b.norm(row[k]) for k in keys) for _,row in data)
        dup=sum(v-1 for v in seen.values())
        if not mapping:check(dup==0,path.name+': duplicate classification keys')
        report[sheet['purpose']].update(data_rows=len(data),columns=header,duplicate_keys=dup)
    key=lambda r:tuple(b.norm(r[k]) for k in b.KEYS)
    budgets={key(r) for _,r in tables['budget']};allocs={key(r) for _,r in tables['phase_allocation']}
    check(budgets==allocs,'Budget/allocation classification coverage differs')
    creative_phases=defaultdict(set)
    for purpose in ['budget','creative']:
        for i,r in tables[purpose]:
            lo,hi=(Decimal(r[k]) for k in ['Suggested Lower Percentile','Suggested Upper Percentile'])
            check(lo.is_finite() and hi.is_finite() and 0<=lo<=hi,f'{purpose}:{i} invalid bounds')
            if purpose=='creative':
                check(lo==int(lo) and hi==int(hi),f'creative:{i} noninteger counts')
                order=int(r['Phase Order']);creative_phases[key(r)].add(order)
                if not 1<=order<=5:check(False,f'creative:{i} invalid phase order');continue
                phase=cfg['phases'][order-1]
                start,end=(phase[k+'_2025'] for k in ['start','end'])
                check(b.norm(r['Peak Sale Phase'])==b.norm(phase['name']) and r['Phase Dates']==start+'~'+end and int(r['Days in Phase'])==(date.fromisoformat(end)-date.fromisoformat(start)).days+1,f'creative:{i} phase metadata mismatch')
    check(set(creative_phases)==budgets and all(p=={1,2,3,4,5} for p in creative_phases.values()),'Creative phases/classification coverage incomplete')
    totals=Counter()
    expected=b.KEYS+[p['name'] for p in cfg['phases']]
    check(report['phase_allocation']['columns']==expected,'Allocation schema must contain four keys and exactly five unique phase columns')
    for i,r in tables['phase_allocation']:
        shares=[Decimal(r[p['name']].removesuffix('%')) for p in cfg['phases']]
        check(all(r[p['name']].endswith('%') for p in cfg['phases']),f'allocation:{i} share missing percent unit')
        total=sum(shares);totals[str(total)]+=1
        check(all(s.is_finite() and 0<=s<=100 for s in shares) and abs(total-100)<=Decimal('.25'),f'allocation:{i} invalid shares/rounding')
    report['phase_allocation']['original_share_totals_percentage_points']=dict(totals)
    regions={r['Ad Sub Region'] for _,r in tables['budget']}
    coverage={}
    for role in ['target','advertiser']:
        purpose=role+'_country_mapping'; records=tables[purpose]
        key,value=(['target_country','target_region'] if role=='target' else ['advertiser_country','Region (5-group)'])
        counts=Counter(row[key] for _,row in records)
        coverage[role]={'duplicate_countries':{k:v for k,v in counts.items() if v>1},
                        'blank_or_null_region_countries':[row[key] for _,row in records if not row[value] or row[value].strip().upper()=='NULL'],
                        'rows_with_blank_country':[i for i,row in records if not row[key]]}
        if role=='target':coverage[role]['regions_absent_from_numeric_tables']=sorted({row[value] for _,row in records}-regions)
    return {'release':cfg['data_release'],'structural_validation_passed':not errors,'errors':errors,'files':report,
            'numeric_keys_consistent_across_three_tables':budgets==allocs==set(creative_phases),
            'classification_groups':len(budgets),'all_five_creative_phases_per_group':all(p=={1,2,3,4,5} for p in creative_phases.values()),
            'country_region_coverage':coverage,
            'mapping_corrections_required':any(v['duplicate_countries'] or v['blank_or_null_region_countries'] or v['rows_with_blank_country'] or v.get('regions_absent_from_numeric_tables') for v in coverage.values()),
            'business_semantics_independently_verified':False,'full_cartesian_coverage_claimed':False,
            'notes':['All six CSVs retain exact source bytes, including duplicates and missing mappings.',
                     'Duplicate country records are ambiguous even if their region values are identical.',
                     'Blank/NULL regions and regions without numeric matches cannot supply Benchmark recommendations.',
                     'Reach (R&F) source rows are retained but do not expand the skill scope.',
                     'Historical shares retain original display rounding; no normalization.']}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path);args=ap.parse_args()
    result=audit();out=json.dumps(result,indent=2)+'\n'
    if args.out:args.out.write_text(out)
    print(out)
    raise SystemExit(0 if result['structural_validation_passed'] else 2)
