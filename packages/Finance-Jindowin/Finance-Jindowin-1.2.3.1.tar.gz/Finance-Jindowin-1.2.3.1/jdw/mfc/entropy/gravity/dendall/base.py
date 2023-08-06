# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from ultron.tradingday import *
from ultron.factor.data.transformer import Transformer
from ultron.strategy.optimize import Optimize
from jdw.kdutils.logger import kd_logger
from jdw.mfc.entropy.gravity.dendall.params import create_params


class Base(object):

    def __init__(self,
                 industry_class,
                 universe_class,
                 yields_class,
                 index_yields_class,
                 horizon=0,
                 offset=0,
                 industry_name='sw',
                 industry_level=1,
                 yield_name='returns',
                 factors_data=None,
                 benchmark=None,
                 universe=None):
        self._index_yields_class = index_yields_class
        self._yields_class = yields_class
        self._industry_class = industry_class
        self._universe_class = universe_class
        self._factors_data = factors_data
        self._benchmark = benchmark
        self._universe = universe
        self._industry_name = industry_name
        self._industry_level = industry_level
        self._horizon = horizon
        self._offset = offset
        self._yield_name = yield_name

    def index_yields(self, begin_date, end_date):
        closing_date = advanceDateByCalendar(
            'china.sse', end_date,
            "{}b".format(self._offset + self._horizon + 1),
            BizDayConventions.Following)
        index_return = self._index_yields_class().yields(
            start_date=begin_date,
            end_date=closing_date,
            offset=self._offset,
            horizon=self._horizon,
            index_code=self._benchmark)
        index_return.rename(columns={'nxt1_ret': 'returns'}, inplace=True)
        return index_return

    def fetch_yields(self, begin_date, end_date, universe=None):
        kd_logger.info("start create yields data")
        yields = self._yields_class()
        if self._yield_name == 'returns':
            closing_date = advanceDateByCalendar(
                'china.sse', end_date,
                "{}b".format(self._horizon + self._offset + 1),
                BizDayConventions.Following)

            yields_data = yields.fetch_returns(universe=universe,
                                               start_date=begin_date,
                                               end_date=closing_date,
                                               horizon=self._horizon,
                                               offset=self._offset,
                                               benchmark=None)
        else:
            yields_data = yields.fetch_yileds(universe=universe,
                                              start_date=begin_date,
                                              end_date=end_date,
                                              name=self._yield_name)
        return yields_data

    def fetch_industry(self, begin_date, end_date, universe=None):
        kd_logger.info("start fetch industry data")
        industry = self._industry_class()
        industry_data = industry.fetch(universe=universe,
                                       start_date=begin_date,
                                       end_date=end_date,
                                       category=self._industry_name,
                                       level=self._industry_level)
        return industry_data

    def create_component(self, begin_date, end_date, universe=None):
        return None

    def create_riskmodel(self, begin_date, end_date, universe=None):
        return None

    def merge(self, industry_data, component_data):
        return None

    def prepare_data(self, begin_date, end_date):
        factor_model, _, risk_exp = self.create_riskmodel(
            begin_date=begin_date,
            end_date=end_date,
            universe=self._universe_class(u_name=self._universe))

        component_data = self.create_component(begin_date=begin_date,
                                               end_date=end_date,
                                               universe=self._universe)

        industry_data = self.fetch_industry(
            begin_date=begin_date,
            end_date=end_date,
            universe=self._universe_class(u_name=self._universe))

        yields_data = self.fetch_yields(
            begin_date=begin_date,
            end_date=end_date,
            universe=self._universe_class(u_name=self._universe))
        total_data = self.merge(industry_data=industry_data,
                                component_data=component_data)
        if risk_exp is not None:
            total_data = total_data.merge(risk_exp, on=['trade_date', 'code'])
        return factor_model, total_data, yields_data

    def create_configure(self, configure):
        return create_params(**configure)

    def create_factors(self, begin_date, end_date):
        yields_data = self._yields_class().fetch_returns(
            universe=self._universe_class(u_name=self._universe),
            start_date=begin_date,
            end_date=end_date,
            horizon=self._horizon,
            offset=self._offset,
            benchmark=None)
        return yields_data

    def prepare_data(self, begin_date, end_date):
        kd_logger.info("start service")
        #factors_data = self.create_factors(begin_date, end_date)
        index_return = None
        if self._benchmark is not None:
            index_return = self.index_yields(begin_date=begin_date,
                                             end_date=end_date)
        factor_model, total_data, yields_data = self.prepare_data(
            begin_date, end_date)
        #factors_data = yields_data.copy()
        #factors_data.rename(columns={'nxt1_ret': 'factor'}, inplace=True)
        total_data = total_data.merge(yields_data, on=['trade_date', 'code'])
        return index_return, factor_model, total_data

    def calculate_result(self,
                         total_data,
                         factor_model,
                         begin_date,
                         end_date,
                         configure,
                         index_returns=None):
        params = self.create_configure(configure)
        optimize = Optimize(alpha_model=None,
                            category=self._category,
                            features=['factor'],
                            begin_date=begin_date,
                            end_date=end_date,
                            risk_model=factor_model,
                            index_return=None,
                            total_data=total_data)
        optimize.rebalance_positions(params)

    def run(self, begin_date, end_date, configure):
        index_returns, factor_model, total_data = self.prepare_data(
            begin_date=begin_date, end_date=end_date)

        self.calculate_result(total_data=total_data,
                              factor_model=factor_model,
                              begin_date=begin_date,
                              end_date=end_date,
                              configure=configure,
                              index_returns=index_returns)
