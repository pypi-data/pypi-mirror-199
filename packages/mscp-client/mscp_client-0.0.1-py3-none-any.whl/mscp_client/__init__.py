

from sqlalchemy import inspect, text
import pandas as pd
class Client:
  def __init__(self, engine):
    self.engine = engine


  def print_cols(self):
    inspector = inspect(self.engine)
    schemas = inspector.get_schema_names()

    for table_name in inspector.get_table_names(schema='mscp'):
      print(table_name)


  def get_dictionary(self,dict_type='all'):
    return_dict={}
    print(dict_type)
    if dict_type=='all':

        return_dict['loggers']={}
        return_dict['stations']={}
        return_dict['measurements']={}
        return_dict['gs_types']={}
        return_dict['sensor_types']={}

        with self.engine.connect() as connection:
            loggers = connection.execute(text("select * from loggers"))
            for logger in loggers:
                  return_dict['loggers'][logger.id]=logger.name        
            stations=connection.execute(text("select * from stations"))
            for station in stations:
                  return_dict['stations'][station.id]=station.name
            measurements=connection.execute(text("select * from measurements"))
            for measurement in measurements:
                  return_dict['measurements'][measurement.id]=measurement.name
            measurements=connection.execute(text("select * from gs_types"))
            for measurement in measurements:
                  return_dict['gs_types'][measurement.id]=measurement.type
            measurements=connection.execute(text("select * from sensor_types"))
            for measurement in measurements:
                  return_dict['sensor_types'][measurement.id]=measurement.type

    if dict_type=='loggers':
      with self.engine.connect() as connection:
        loggers=connection.execute(text("select * from loggers"))
        for logger in loggers:
              return_dict[logger.id]=logger.name
    if dict_type=='stations':
      with self.engine.connect() as connection:
        loggers=connection.execute(text("select * from stations"))
        for logger in loggers:
              return_dict[logger.id]=logger.name
    if dict_type=='measurements':
      with self.engine.connect() as connection:
        loggers=connection.execute(text("select * from measurements"))
        for logger in loggers:
              return_dict[logger.id]=logger.name
    return return_dict

  def render_legacy(self,df):

      #map the ids to the names.
      df["logger_id"] = df["logger_id"].map(self.get_dictionary("loggers"))
      df["station_id"] = df["station_id"].map(self.get_dictionary("stations"))
      df["measurement_id"] = df["measurement_id"].map(self.get_dictionary("measurements"))

      # create a new column that combines measurement_id and port_number
      df['measurement_port'] = df['measurement_id'] + ' port ' + df['port_number'].astype(str)

      # pivot the data frame for values
      pivot = df.pivot_table(index=['logger_id', 'station_id', 'timestamp'],
                              columns='measurement_port',
                              values='value')

      # pivot the data frame for qa_codes_id
      qa_pivot = df.pivot_table(index=['logger_id', 'station_id', 'timestamp'],
                              columns='measurement_port',
                              values='qa_codes_id',
                              aggfunc=lambda x: ' '.join(str(v) for v in x))

      # reset the index for both pivot tables
      pivot = pivot.reset_index()
      qa_pivot = qa_pivot.reset_index()

      # join the two pivot tables on the index columns
      result = pd.merge(pivot, qa_pivot, on=['logger_id', 'station_id', 'timestamp'])
      return result
