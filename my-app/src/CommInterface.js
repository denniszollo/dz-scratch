import React from 'react';
import { Button, Popover, PopoverHeader, PopoverBody, Progress} from 'reactstrap';


class CommInterfaceHeader extends React.Component {
  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);
    this.state = {
      popoverOpen: false
    };
  }

  toggle() {
    this.setState({
      popoverOpen: !this.state.popoverOpen
    });
  }

  render() {
    return (
      <div>
        <Button id={this.props.interfaceName} onClick={this.toggle}>
          {this.props.interfaceName}
        </Button>
        <Popover placement="bottom" isOpen={this.state.popoverOpen} 
        target={this.props.interfaceName} toggle={this.toggle}>
          <PopoverHeader>{this.props.userFacingInterfaceName}</PopoverHeader>
          <PopoverBody><detailed_desc>
          {this.props.interfaceDesc}</detailed_desc></PopoverBody>
        </Popover>
      </div>
    );
  }
}


class CommInterfaceDetail extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let ratio = Number(this.props.bps/Number(this.props.maxbps));
    let style = "info";
    if (ratio > 0.75) 
    {
      style="warning";
    }
    if (ratio > 0.9) 
    {
      style="danger";
    }
    return (
      <div>
          Nominal Data Rate: {this.props.bps} Bits Per Second {"\n"}
          Interface Max Rate: {this.props.maxbps} Bits Per Second
          <Progress value={ratio * 100} color={style} />
      </div>
      );
    }
}

export {CommInterfaceHeader, CommInterfaceDetail}