import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

const SensorDataChart = () => {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5654/db/tql/neo-apps/live-sensor/get-sensor-data.tql?tag=TAG-SENSOR4');
        const data = await response.json();
        if (data.success && data.data && data.data.rows) {
          const formattedData = data.data.rows.map(row => ({
            time: row[0], // datetime
            value: row[1] // double
          }));
          setSensorData(formattedData);
        }
      } catch (error) {
        console.error('Failed to fetch sensor data:', error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const getOption = () => ({
    title: {
      text: 'Data Samples',
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: sensorData.map(data => data.time),
    },
    yAxis: {
      type: 'value',
    },
    series: [{
      data: sensorData.map(data => data.value),
      type: 'line',
      smooth: true,
    }],
  });

  return <ReactECharts option={getOption()} style={{ height: '400px', width: '100%' }} />;
};

export default SensorDataChart;
