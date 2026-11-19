#!/usr/bin/env python3
"""Offline behavioral checks; no real account or network calls."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import benchmark
import plan_math as m


class MathChecks(unittest.TestCase):
    def test_tiers_and_unknown(self):
        self.assertEqual([m.spend_tier(x)['tier'] for x in ['999.99',1000,'4999.99',5000]], ['T3','T2','T2','T1'])
        self.assertIsNone(m.spend_tier(5000, complete=False)['tier'])
        self.assertIsNone(m.spend_tier(None)['tier'])
        with self.assertRaises(ValueError): m.spend_tier(-1)

    def test_actual_spend_not_current_budget(self):
        base = dict(bau_total=900, bau_complete=True, lower_multiplier=2, upper_multiplier=3, currency='USD')
        out = m.budget(dict(base, current_budget=40))
        self.assertEqual(out['recommended_range_unrounded'], ['60', '90'])
        self.assertEqual(out['prefilled_budget'], '60')
        self.assertEqual(out['delta'], '20')
        for current in [60,75,100]:
            out = m.budget(dict(base, current_budget=current))
            self.assertEqual(out['status'], 'unchanged_no_budget_prompt')
            self.assertFalse(out['prompt_existing_budget'])

    def test_historical_fallbacks(self):
        self.assertEqual(m.budget(dict(bau_total=0, bau_complete=True))['status'], 'ask_investment_range')
        self.assertEqual(m.budget(dict(bau_total=900,bau_complete=False,historical_bau_daily_budget=25))['prefilled_budget'], '25')

    def test_brand_best_practice_without_bau(self):
        base = dict(bau_total=0, bau_complete=True, brand_new_campaign=True,
                    best_practice_applicable=True, best_practice_budget=160, currency='USD')
        self.assertEqual(m.budget(base)['prefilled_budget'], '160')
        self.assertEqual(m.budget(base)['source'], 'Objective_Best_Practice_verified_registered_region')
        self.assertEqual(m.budget(dict(base, best_practice_applicable=False))['status'], 'ask_investment_range')
        self.assertEqual(m.budget(dict(base, brand_new_campaign=False))['status'], 'ask_investment_range')
        self.assertEqual(m.budget(dict(base, bau_total=900, lower_multiplier=2, upper_multiplier=3))['prefilled_budget'], '60')

    def test_precision_and_errors(self):
        out = m.budget(dict(bau_total=100,bau_complete=True,lower_multiplier=1,upper_multiplier=2,currency_step='0.05'))
        self.assertEqual(out['prefilled_budget'], '3.35')
        invalid = dict(bau_total=900,bau_complete=True,lower_multiplier=3,upper_multiplier=2)
        self.assertEqual(m.budget(invalid)['status'], 'ask_investment_range')
        self.assertIsNotNone(m.budget(invalid)['benchmark_issue'])

    def creative_input(self):
        return dict(schedules=[dict(start_date='2026-11-12',end_date='2026-11-22')],
                    phase_intervals=[dict(phase_order=1,lower=31,upper=77),dict(phase_order=2,lower=28,upper=70),dict(phase_order=3,lower=32,upper=79)],
                    available_count=20, same_scope=True, count_complete=True)

    def test_creative_max_not_sum(self):
        out=m.creative(self.creative_input())
        self.assertEqual(out['covered_phases'],[1,2,3])
        self.assertEqual(out['reference'],[32,79])
        self.assertEqual(out['supplement'],[12,59])
        self.assertFalse(out['blocks_creation_due_to_count'])
        for available,gap in [(40,[0,39]),(79,[0,0]),(100,[0,0])]:
            self.assertEqual(m.creative(dict(self.creative_input(),available_count=available))['supplement'],gap)

    def test_schedule_union_and_remaining_dates(self):
        schedules=[dict(start_date='2026-11-15',end_date='2026-11-16'),dict(start_date='2026-11-26',end_date='2026-11-30')]
        self.assertEqual(m.covered_phases(schedules),[1,2,5])
        self.assertEqual(m.covered_phases(schedules,'2026-11-16'),[2,5])
        self.assertEqual(m.covered_phases(schedules,'2026-12-01'),[])
        self.assertEqual(m.covered_phases([dict(start_date='2025-11-13',end_date='2025-11-16')]),[])

    def test_creative_partial_and_dedup(self):
        base=self.creative_input()
        self.assertIsNone(m.creative(dict(base,same_scope=False))['supplement'])
        self.assertIsNone(m.creative(dict(base,count_complete=False))['supplement'])
        out=m.creative(dict(base,phase_intervals=base['phase_intervals'][:2]))
        self.assertEqual(out['missing_phases'],[3]);self.assertIsNone(out['reference'])
        del base['available_count'];base['verified_available_ids']=['video:1','video:1','post:2']
        self.assertEqual(m.creative(base)['available_count'],2)

    def test_phase_share_rounding(self):
        for values in [[18.9,14.6,20.5,16.5,29.5],[18.8,14.8,20.8,16.0,29.5],[19,12.7,20,15.9,32.5]]:
            out=m.shares(values)
            self.assertIn(out['status'],['totals_100','display_rounding_difference'])
            self.assertFalse(out['normalize'])
        self.assertEqual(m.shares([10,10,10,10,10])['status'],'verify_source_total')
        self.assertEqual(m.shares([20,20,None,20,20])['status'],'verify_missing_phase_shares')


class SourceChecks(unittest.TestCase):
    def test_header_order_and_exact_lookup(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'budget.csv'
            header='Objective Type EN,Ad Sub Region,Industry v3.2 L2 Name,Spend Tier,Suggested Upper Percentile,Suggested Lower Percentile\n'
            row='Traffic,SEA,Beauty and Care,T3 0-999.99,9.02,3.63\n'
            path.write_text(header+row)
            key={'Objective Type EN':'Traffic','Ad Sub Region':'SEA','Industry v3.2 L2 Name':'Beauty and Care','Spend Tier':'T3 0-999.99'}
            out=benchmark.lookup(path,key)
            self.assertEqual(out['status'],'unique')
            self.assertEqual(out['matches'][0]['values']['Suggested Lower Percentile'],'3.63')
            path.write_text(header+row+row)
            self.assertEqual(benchmark.lookup(path,key)['status'],'ambiguous')
            key['Ad Sub Region']='Unknown'
            self.assertEqual(benchmark.lookup(path,key)['status'],'missing')

    def test_duplicate_headers_and_missing_creative_phase(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'bad.csv'
            key={'Industry v3.2 L2 Name':'Ordinary Cosmetics','Objective Type EN':'Traffic','Ad Sub Region':'SEA','Spend Tier':'T3 0-999.99'}
            path.write_text(','.join(key)+',Black Friday,Black Friday\n'+','.join(key.values())+',20%,20%\n')
            with self.assertRaises(ValueError): benchmark.lookup(path,key)
        with self.assertRaises(ValueError): benchmark.lookup(benchmark.source('creative'),key)

    def test_real_release_end_to_end(self):
        key={'Industry v3.2 L2 Name':'Ordinary Cosmetics','Objective Type EN':'Traffic','Ad Sub Region':'SEA','Spend Tier':'T3 0-999.99'}
        budget=benchmark.lookup(benchmark.source('budget'),key)
        self.assertEqual(budget['status'],'unique')
        values=budget['matches'][0]['values']
        result=m.budget(dict(bau_total=900,bau_complete=True,lower_multiplier=values['Suggested Lower Percentile'],upper_multiplier=values['Suggested Upper Percentile'],current_budget=40))
        self.assertEqual(result['prefilled_budget'],str(m.money(m.Decimal(30)*m.Decimal(values['Suggested Lower Percentile']),m.Decimal('.01'))))
        self.assertEqual([m.Decimal(v) for v in result['recommended_range_unrounded']],[m.Decimal(30)*m.Decimal(values[k]) for k in ['Suggested Lower Percentile','Suggested Upper Percentile']])
        intervals=[]
        for phase in (1,2,3):
            out=benchmark.lookup(benchmark.source('creative'),dict(key,**{'Phase Order':str(phase)}))
            self.assertEqual(out['status'],'unique')
            row=out['matches'][0]['values']
            intervals.append(dict(phase_order=phase,lower=row['Suggested Lower Percentile'],upper=row['Suggested Upper Percentile']))
        expected=[max(int(i['lower']) for i in intervals),max(int(i['upper']) for i in intervals)]
        out=m.creative(dict(schedules=[dict(start_date='2026-11-12',end_date='2026-11-22')],phase_intervals=intervals,available_count=20,same_scope=True,count_complete=True))
        self.assertEqual(out['reference'],expected)
        allocation=benchmark.lookup(benchmark.source('phase_allocation'),key)
        self.assertEqual(allocation['status'],'unique')
        values=allocation['matches'][0]['values']
        self.assertIn(m.shares([values[p['name']].rstrip('%') for p in benchmark.config()['phases']])['status'],['totals_100','display_rounding_difference'])
        self.assertEqual(benchmark.lookup(benchmark.source('budget'),dict(key,**{'Ad Sub Region':'NOT_A_SOURCE_REGION'}))['status'],'missing')

    def test_independent_country_roles_and_multitarget(self):
        self.assertEqual(benchmark.country('DE','target')['target_region'],'DACH')
        self.assertEqual(benchmark.country('GB','target')['target_region'],'UKIE')
        self.assertEqual(benchmark.country('US','advertiser')['mapped_value'],'NA')
        self.assertEqual(benchmark.country('US','target')['status'],'ambiguous')
        self.assertIsNone(benchmark.country('US','target')['target_region'])
        self.assertEqual(benchmark.country('SG','target')['status'],'ambiguous')
        results=[benchmark.country(c,'target') for c in ['DE','GB','US']]
        self.assertEqual([x['status'] for x in results],['unique','unique','ambiguous'])
        self.assertNotIn('mapped_value',results[0])
        self.assertNotIn('target_region',benchmark.country('US','advertiser'))

    def test_mapping_missing_exact_and_blank(self):
        self.assertEqual(benchmark.country('NOT_A_COUNTRY','target')['status'],'missing')
        self.assertEqual(benchmark.country('de','target')['status'],'missing')
        self.assertEqual(benchmark.country('AQ','advertiser')['status'],'unmapped')
        with self.assertRaises(ValueError):benchmark.country('US','unknown')
        with self.assertRaises(ValueError):benchmark.country('','advertiser')
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'mapping.csv'
            path.write_text('advertiser_country,Region (5-group)\nUS,NA\nUS,NA\n')
            with patch.object(benchmark,'source',return_value=path):
                out=benchmark.country('US','advertiser')
                self.assertEqual(out['status'],'ambiguous');self.assertIsNone(out['mapped_value'])
            path.write_text('advertiser_country,Region (5-group)\nUS,\n')
            with patch.object(benchmark,'source',return_value=path):
                self.assertEqual(benchmark.country('US','advertiser')['status'],'unmapped')
        with self.assertRaises(ValueError):benchmark.country_rows([['target_country','target_country'],['DE','DACH']],'target')

    def test_target_mapped_budget_and_unsupported_buying_type(self):
        target=benchmark.country('DE','target')
        key={'Industry v3.2 L2 Name':'Ordinary Cosmetics','Objective Type EN':'Traffic','Ad Sub Region':target['target_region'],'Spend Tier':'T3 0-999.99'}
        self.assertEqual(benchmark.lookup(benchmark.source('budget'),key)['status'],'unique')
        self.assertEqual(benchmark.country('US','advertiser')['mapped_value'],'NA')
        with self.assertRaises(ValueError):
            benchmark.lookup(benchmark.source('budget'),dict(key,**{'Objective Type EN':'Reach (R&F)'}))

    def test_invalid_web_response(self):
        with self.assertRaises(ValueError):benchmark.csv_rows('<!DOCTYPE html><html>Sign in</html>')
        with self.assertRaises(ValueError):benchmark.csv_rows('unavailable')


if __name__=='__main__':
    unittest.main(verbosity=2)
