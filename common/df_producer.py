# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 下午5:08
# @Author  : Mat
import pickle
from kafka import KafkaProducer
import logging
from kafka import SimpleClient
from common.db_craw_reader import CrawReader
from util.db_util import DBUtil
from util.redis_util import RedisUtil
import logging as log
from common.craw_table_profile import CrawTableProfile


class DFProducer:
    def __init__(self, bootstrap_servers):
        self.kafka_client = SimpleClient(bootstrap_servers)
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10),
            retries=3,
            max_block_ms=60 * 1000,
            value_serializer=lambda m: pickle.dumps(m)
        )

    def produce(self, reader):
        data_df = reader.read_data()
        if data_df.empty:
            log.info('本次数据采集的数量为0...')
            return
        key = reader.get_table_profile().get_key()
        bkey = bytes(key, encoding="utf8")
        tpc = reader.get_table_profile().get_pub_topic()
        tp_part = len(self.kafka_client.get_partition_ids_for_topic(tpc))
        for idx, row in data_df.iterrows():
            part = idx % tp_part
            self.producer.send(tpc, value=row, key=bkey, partition=part).add_errback(
                self.on_send_error, key, tpc)
        self.producer.flush()
        log.info('成功发送数据表key【{}】的数据【{}】条到kafka...'.format(key, data_df.shape[0]))

    def on_send_error(self, ex, key, topic):
        logging.error('数据表【{}】的数据发送kafka【{}】失败！！！'.format(key, topic), ex)


if __name__ == '__main__':
    from util.config_util import ConfigUtil

    log.basicConfig(level=log.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
    config_file_path = '../../conf/db_config_inner.ini'

    db_set_dict = ConfigUtil.read_conf_values(config_file_path, 'redis')
    client = RedisUtil.get_redis_client(db_set_dict)
    c_db_set_dict = ConfigUtil.read_conf_values(config_file_path, 'hs_config')
    r_db_set_dict = ConfigUtil.read_conf_values(config_file_path, 'stgy_postgres')
    # r_db_set_dict = ConfigUtil.read_conf_values(config_file_path, 'vaon_mysql')
    w_db_set_dict = ConfigUtil.read_conf_values(config_file_path, 'hege_ods')

    c_engine = DBUtil.get_db_engine('mysql', c_db_set_dict)
    r_engine = DBUtil.get_db_engine('postgres', r_db_set_dict)
    # r_engine = DBUtil.get_db_engine('mysql', r_db_set_dict)
    w_engine = DBUtil.get_db_engine('mysql', w_db_set_dict)
    table_profile = CrawTableProfile.get_table_profile(c_engine, 'stgy',
                                                       'core.t_book_strategy_earnings',
                                                       'hege_ods',
                                                       'hedge_ods.temp_stgy_strategy_earnings')
    reader = CrawReader(r_engine, table_profile, client)
    bootstrap_servers = ConfigUtil.read_conf_lvalue(config_file_path, 'kafka', 'bootstrap_servers')
    df_producer = DFProducer(bootstrap_servers)
    df_producer.produce(reader)




