## This is a Case Study of Vibration Data Analysis Using FFT

Please open the 'realtime-fft.wrk' and follow the directions to run this demo.

### Tutorial

- realtime-fft.wrk: worksheet for setting up this demo

### Data Schema
- schema.sql: table schema for your convenience

### Data Insertion
- insert-auto-fft-x.tql: insert 1000Hz vibration data for the X axis with some noise
- insert-auto-fft-y.tql: insert 1000Hz vibration data for the Y axis with some noise
- insert-auto-fft-z.tql: insert 1000Hz vibration data for the Z axis with some noise

### Real-Time Data Statistical Analysis
- realtime-data.html: display the statistics page
- realtime-data-raw.tql: generate the raw chart for each axis
- realtime-data-stat.tql: generate the statistics for each axis

### Customized Data Statistical Analysis
- custom-data.html: display the customized statistics page
- custom-data-raw.tql: generate the raw chart for each axis
- custom-data-stat.tql: generate the statistics for each axis

### Real-Time FFT Analysis
- fft-2d-x.tql: generate a single FFT 2D chart on the X axis for the last 1 second
- fft-2d-y.tql: generate a single FFT 2D chart on the Y axis for the last 1 second
- fft-2d-z.tql: generate a single FFT 2D chart on the Z axis for the last 1 second
- fft-3d-x.tql: generate multiple FFT 3D charts on the X axis for the last 10 seconds
- fft-3d-y.tql: generate multiple FFT 3D charts on the Y axis for the last 10 seconds
- fft-3d-z.tql: generate multiple FFT 3D charts on the Z axis for the last 10 seconds
- realtime-fft.dsh: visualize the real-time X, Y, Z axis data
- realtime-fft.html: show all FFT charts in 2D and 3D using the above TQL files
- realtime-fft.taz: analysis tool for FFT in any data range

### Customized FFT Analysis
- custom-fft.html: display your own custom FFT chart
- custom-fft-3d.tql: generate a single FFT in customized mode
- custom-fft-3d-download.tql: download the CSV file for the customized FFT data