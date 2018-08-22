import React, { Component } from 'react';
import { Col, Collapse, Button, CardBody, Card } from 'reactstrap';







class SbpMsgDesc extends Component {
  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);
    this.state = { collapse: false };
  }

  toggle() {
    this.setState({ collapse: !this.state.collapse });
  }

  render() {
    return (
      <div>
            <Button color="primary" onClick={this.toggle} style={{ marginBottom: '1rem' } } align='left'>{this.props.msgName}</Button>
        <Collapse isOpen={this.state.collapse}>
          <Card>
            <CardBody>
            <h4>{this.props.shortDesc}</h4>
            <var text-align='left'>{this.props.longDesc}</var>
            </CardBody>
          </Card>
        </Collapse> 
      </div>
    );
  }
}

export {SbpMsgDesc}