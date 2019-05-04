import SensorDB as sdb
import datetime
import bokeh.plotting as bp

TEST_ENTRY = {
    'comment': 'testadelphia'
}

s = sdb.SensorDBI()

# s.add_to_testing(TEST_ENTRY)
tstop = datetime.datetime.now()
tstart = (tstop - datetime.timedelta(days=4))
times, tempc, tempf = s.get_temp_readings(tstart, tstop, 'Pecan')

bp.output_file('test.html')
p = bp.figure(title='Tempf vs Time', x_axis_type='datetime', x_axis_label='time', y_axis_label='Temp [F]')
p.line(times, tempf, legend='Tempf/Tempc', line_width=2)
bp.show(p)