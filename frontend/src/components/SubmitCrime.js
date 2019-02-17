import React from 'react';
import {geolocated} from 'react-geolocated';
import {Form,Button,Container} from "react-bootstrap";

class SubmitCrime extends React.Component {

  handleSubmit(e){
    // this.refs.
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
                ? <div>
                  <label>Location: Latitude={this.props.coords.latitude} , Longitude={this.props.coords.longitude}</label><br/>
                  <Button type="submit">Submit</Button>
                </div>
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
