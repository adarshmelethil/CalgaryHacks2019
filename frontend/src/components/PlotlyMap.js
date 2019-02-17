import React from 'react';
import Plot from 'react-plotly.js';


class PlotlyMap extends React.Component {

  // constructor(props) {
  //   super(props);
  //
  //   this.state = {
  //     isLoading: true,
  //     data: [],
  //   };
  // }
  //
  //
  // componentDidMount() {
  //   fetch('/get_all_crimes', {
  //       headers:{ "Content-Type": "application/json" },
  //       method: 'GET',
  //   }).then(response => this.updateUI(response));
  // }
  //
  // updateUI = response => {
  //   response
  //     .text()
  //     .then(body => {
  //         let rawData = JSON.parse(body);
  //         // let rawData =[
  //         //   {
  //         //     "crime": "Breaking & Entering/Robbery",
  //         //     "description": "asdf",
  //         //     "lat": 51.086794,
  //         //     "lon": -114.1297654,
  //         //     "time": 1550384173790
  //         //   },
  //         //   {
  //         //     "crime": "Breaking & Entering/Robbery",
  //         //     "description": "asdf",
  //         //     "lat": 51.087800,
  //         //     "lon": -114.1298690,
  //         //     "time": 1550384197977
  //         //   }
  //         // ];
  //
  //         let crimeTypes = rawData.map( record => record.crime);
  //         crimeTypes = [...new Set(crimeTypes)];
  //
  //         let data = crimeTypes.map( (type,i) => {
  //           let lat =[];
  //           let lon =[];
  //
  //           rawData.filter(record => record.crime === type).forEach( record => {
  //             lat.push(record.lat);
  //             lon.push(record.lon);
  //           });
  //
  //           return {
  //             type:'scattermapbox',
  //             lat:lat,
  //             lon:lon,
  //             text:type,
  //             mode:'markers',
  //             marker: {
  //               size:14,
  //               color:COLORS[i]
  //             },
  //             name:type,
  //           }
  //         });
  //         console.log(data);
  //
  //         this.setState({
  //           data: data,
  //           isLoading: false
  //         });
  //       }
  //     );
  // };

  render() {
    return(
      <div id="helloWorld" style={{height:"90vh",width:"100%"}}></div>
    )
  }
}


export default  PlotlyMap;
