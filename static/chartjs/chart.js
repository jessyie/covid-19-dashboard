// Function to fetch and update chart data
function updateCharts(selectedCase, continent) {

  fetch(`/update_charts?case=${selectedCase}&continent=${''}`)
  .then(response => response.json())
  .then(data => {
    
    // Update chart configuration and data based on the fetched data

    document.querySelector('#casesTotal').innerHTML = data.tSum + " : TOTAL CASES";
    document.querySelector('#map-container').innerHTML = data.world_map;
    
    // Get the select element
    var selectElement = document.getElementById("continentSelection");

    // Store the currently selected region
    var selectedContinent = selectElement.value;

    // Get the "Region" option element
    // var regionOption = document.getElementById("regionOption");

    // Clear existing options except the "Region" option
    while (selectElement.options.length > 1) {
        selectElement.remove(1);
    }

    //Iterate over the fetched data and create new options
    for (var i = 0; i < data.graph1AX.length; i++) {
        var option = document.createElement("option");
        option.textContent = data.graph1AX[i];
        selectElement.appendChild(option);
    }

    // Set the value of the select element to the stored selected region
    // selectElement.value = selectedRegion;

    // // Ensure the "Region" option is always the first option
    // selectElement.insertBefore(regionOption, selectElement.options[0]);


    chart1.update({
      chart: {
        type: 'column'
    },
    title: {
        text: 'TOTAL RECOREDED CASES',
        align: 'left'
    },
    xAxis: {
        categories: data.graph1AX,
        crosshair: true,
        accessibility: {
            description: 'CONTINENTS'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'TOTAL CASES'
        }
    },
    tooltip: {
        valueSuffix: ''
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    credits: {
        enabled: false
     },
    series: [{
        name: 'TOTAL CASES',
        data: data.graph1AY
      }]
    });

    
    
  })

    
  
};


// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function changeChartCase() {
  const caseSelector = document.querySelector("#caseSelection")
  const continentSelector = document.querySelector("#continentSelection")
  activeCase = caseSelector.value || 'Total_Confirmed'
  activeContinent = continentSelector.value || 'Africa'
  updateCharts(activeCase, activeContinent);
  
}


  // Function to fetch and update chart data
function updateCharts2(case1, selectedContinent) {

  fetch(`/update_charts?case=${case1}&continent=${selectedContinent}`)
  .then(response => response.json())
  .then(data => {
    
    // Update chart configuration and data based on the fetched data

    document.querySelector('#casesTotal').innerHTML = data.tSumB + " : TOTAL CASES";
    document.querySelector('#map-container').innerHTML = data.world_map2;

    var selectElement = document.getElementById("continentSelection");

    // Store the currently selected region
    var selectedContinent = selectElement.value;

    // Get the "Region" option element
    // var regionOption = document.getElementById("regionOption");

    // Clear existing options except the "Region" option
    while (selectElement.options.length > 1) {
        selectElement.remove(1); 

      }

    //Iterate over the fetched data and create new options
    for (var i = 0; i < data.graph1AX.length; i++) {
        var option = document.createElement("option");
        option.textContent = data.graph1AX[i];
        selectElement.appendChild(option);
    }

    // Set the value of the select element to the stored selected region
    selectElement.value = selectedContinent;
    


    chart1.update({
      chart: {
        type: 'bar',
        style: {
          fontSize: '15px',
          
        }
      },
      title: {
        text: 'TOTAL RECOREDED CASES',
        align: 'left'
      },

      xAxis: {
        categories: data.graph1BX,
        scrollbar: {
          enabled: true
        },
        min: 0,
        max: 4,
        title: {
          text: 'COUNTRIES'
        },
        gridLineWidth: 1,
        tickLength: 0,
        lineWidth: 0
      },
      yAxis: {
        min: 0,
        title: {
          text: 'TOTAL CASES',
          align: 'high'
        },
        labels: {
          overflow: 'justify'
        },
        gridLineWidth: 0
      },
      tooltip: {
        valueSuffix: '' 
      },
      plotOptions: {
        bar: {
          borderRadius: '50%',
          dataLabels: {
            enabled: true
          },
          groupPadding: 0.1
        }
      },
      legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 30,
        floating: true,
        borderWidth: 1,
        backgroundColor:
        Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        shadow: true
      },
      credits: {
        enabled: false
      },
      series: [{
        name: 'Total Cases',
        data: data.graph1BY
      }]
    });

    
  })


};


// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function changeChartContinent() {
  const caseSelector = document.querySelector("#caseSelection")
  const continentSelector = document.querySelector("#continentSelection")
  activeContinent = continentSelector.value || 'Africa'
  activeCase = caseSelector.value ||'Total_Confirmed'
  updateCharts2(activeCase, activeContinent);  
}
