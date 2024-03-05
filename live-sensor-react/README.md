# Getting Started with live-sensor-react

## Running the timer tql in live-sensor

To run this demo, please execute the timer tqil  in live-sensor as described in ./live-sensor/live-sensor.wrk

## `npm install`

To install necessary packages, run this command.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Machbase NEO URL check 

If you can't see the chart running, please check the NEO DBMS TQL url.
By default, the URL is in source code ./src/SensorDataChart.js that is http://127.0.0.1:5654/db/tql/neo-apps/live-sensor/get-sensor-data.tql

