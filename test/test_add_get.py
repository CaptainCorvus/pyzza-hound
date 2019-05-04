import SensorDB
import datetime
import bokeh.plotting as bp

TEST_ENTRY = {
    'comment': 'testadelphia'
}

data_interface = SensorDB.DataInterface()

# s.add_to_testing(TEST_ENTRY)
tstop = datetime.datetime.now()
tstart = (tstop - datetime.timedelta(hours=36))
times, tempc, tempf = data_interface.get_temp_readings(tstart, tstop, 'Pecan')

bp.output_file('test.html')
p = bp.figure(title='Tempf vs Time', x_axis_type='datetime',
              plot_height=500, plot_width=800,
              x_axis_label='time', y_axis_label='Temp [F]')
p.scatter(times, tempf, legend='Temperature', line_width=2)
bp.show(p)