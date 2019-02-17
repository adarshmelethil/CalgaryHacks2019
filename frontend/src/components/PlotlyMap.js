import React from 'react';
import Plot from 'react-plotly.js';

class PlotlyMap extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      data: [],
    };
  }

  componentDidMount() {
    fetch('/get_all_crimes', {
        headers:{ "Content-Type": "application/json" },
        method: 'GET',
    }).then(response => this.updateUI(response));
  }

  updateUI = response => {
    response
      .text()
      .then(body => {
          // let rawData = JSON.parse(body);
          let rawData =[
            {
              "crime": "Breaking & Entering/Robbery",
              "description": "asdf",
              "lat": 51.086794,
              "lon": -114.1297654,
              "time": 1550384173790
            },
            {
              "crime": "Breaking & Entering/Robbery",
              "description": "asdf",
              "lat": 51.087800,
              "lon": -114.1298690,
              "time": 1550384197977
            }
          ];

          let crimeTypes = rawData.map( record => record.crime);
          crimeTypes = [...new Set(crimeTypes)];

          let data = crimeTypes.map( type => {
            let lat =[];
            let lon =[];

            rawData.filter(record => record.crime === type).forEach( record => {
              lat.push(record.lat);
              lon.push(record.lon);
            });

            return {
              type:'scattermapbox',
              lat:lat,
              lon:lon,
              mode:'markers',
              marker: {
                size:14
              },
              name:type
            }
          });
          console.log(data);

          this.setState({
            data: data,
            isLoading: false
          });
        }
      );
  };

  render() {
    const { data, isLoading } = this.state;
    return (
      !isLoading
          ?<Plot style={{height:"90vh",width:"100%"}}

          data={data}
          layout={{
            title: 'Crime Activity',
            font: {
              color: 'white'
            },
            dragmode: 'zoom',
            mapbox: {
              center: {
                lat:51.05,
                lon:-114.07,
              },
              domain: {
                x: [0, 1],
                y: [0, 1]
              },
              style: 'dark',
              zoom: 9.5
            },
            margin: {
              r: 20,
              t: 40,
              b: 20,
              l: 20,
              pad: 0
            },
            paper_bgcolor: 'black',
            plot_bgcolor: 'black',
            showlegend: true,
            annotations: [{
              x: 0,
              y: 0,
              xref: 'paper',
              yref: 'paper',
              text: 'Source: NASA',
              showarrow: false
            }]
          }}
          config={{
            mapboxAccessToken: 'pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA'
          }}
          />
          :<p>"Loading data"</p>


    );
  }
}


export default  PlotlyMap;
