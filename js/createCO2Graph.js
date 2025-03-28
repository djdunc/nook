async function createCO2Graph() {
    try {
      const response = await fetch('https://global-warming.org/api/co2-api');
      const data = await response.json();
  
      const years = data.co2.map(item => `${item.year}-${item.month}-${item.day}`);
      const cycleValues = data.co2.map(item => parseFloat(item.cycle));
      const trendValues = data.co2.map(item => parseFloat(item.trend));
  
      const latestCycle = cycleValues[cycleValues.length - 1];
      const latestTrend = trendValues[trendValues.length - 1];
      const latestDate = years[years.length -1];
      const latestYear = latestDate.split('-')[0];
  
      const ctx = document.getElementById('co2Chart').getContext('2d');
      const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: years,
          datasets: [{
            label: 'CO2 Cycle (ppm)',
            data: cycleValues,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false,
          }, {
            label: 'CO2 Trend (ppm)',
            data: trendValues,
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: false,
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'CO2 Concentration (ppm)'
              }
            },
            x: {
              ticks: {
                callback: function(value, index, values) {
                  // Extract and return only the year
                  return years[index].split('-')[0];
                },
                autoSkip: true,
                maxTicksLimit: 10 // Adjust as needed
              },
              title: {
                display: true,
                text: 'Date'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: `CO2 Concentration Over Time -  Today = ${latestTrend} ppm`,
              padding: {
                top: 10,
                bottom: 30
              }
            },
            legend: { // Add this to hide the legend
              display: false,
            },
          }
        }
      });
    } catch (error) {
      console.error('Error fetching or plotting data:', error);
    }
  }
  
  createCO2Graph();