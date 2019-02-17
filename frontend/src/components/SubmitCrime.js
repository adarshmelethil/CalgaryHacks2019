import React from 'react';
import {geolocated} from 'react-geolocated';
import {Form,Button,Container} from "react-bootstrap";

class SubmitCrime extends React.Component {

  handleSubmit(e){
    e.preventDefault();
    const data = {
      "crime": this.refs.crime.value,
      "description": this.refs.description.value,
      "lat": this.props.coords.latitude,
      "lon": this.props.coords.longitude,
      "time": new Date().getTime()
    };

    console.log(data);


    return fetch("web/submit_crime", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
      .then(response => {
        if (response.ok){
          alert("Success. Data has been submitted.")
        }else{
          alert("Failed to submit data.")
        }
      });

  }
  render() {
    return !this.props.isGeolocationAvailable
      ? <div>Your browser does not support Geolocation</div>
      : !this.props.isGeolocationEnabled
        ? <div>Geolocation is not enabled</div>
        :
          <Container>
            <br/>
            <Form
              onSubmit={e => this.handleSubmit(e)}>
              <Form.Group controlId="exampleForm.ControlSelect1">
                <Form.Label>Crime Type</Form.Label>
                <Form.Control as="select" ref="crime">
                  <option>Breaking & Entering/Robbery</option>
                  <option>Violence</option>
                  <option>Physical Disorder</option>
                  <option>Theft from Vehicle</option>
                  <option>Illegal Drug Activity</option>
                </Form.Control>
              </Form.Group>
              <Form.Group controlId="exampleForm.ControlTextarea1">
                <Form.Label>Description</Form.Label>
                <Form.Control as="textarea" rows="3" ref="description"/>
              </Form.Group>
              {this.props.coords
                ? <p>Location: Latitude={this.props.coords.latitude} , Longitude={this.props.coords.longitude}<br/>
                    <Button type="submit">Submit</Button>
                  </p>
                : <p>Loading location data. Please wait!</p>
              }
            </Form>
          </Container>
  }
}

export default geolocated({
  positionOptions: {
    enableHighAccuracy: false,
  },
  userDecisionTimeout: 5000,
})(SubmitCrime);
