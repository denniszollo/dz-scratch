import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import 'react-bootstrap-table/dist/react-bootstrap-table-all.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { Collapse, Button, CardBody, Card } from 'reactstrap';
import {SbpTable} from './SbpTable'
import {CommInterfaceHeader, CommInterfaceDetail} from './CommInterface.js';
import {SbpMsgTable} from './MsgTable'

//for (let msg in SbpMsgTable) {
 // console.log(SbpMsgTable[msg])
//}

var SbpMsgs= [{
      msgId: 522,
      name: "MsgPosLLH",
      msggrouping: 'navigation'
  }, {
      msgId: 521,
      name: "MsgPosECEF",
      msggrouping: 'navigation'
  }];



class App extends Component {
  render() {
    let bps = 120000
    let maxbps = 115200
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <div className="CommInterface">
        <CommInterfaceDetail interfaceName="UART1" userFacingInterfaceName="Primary Serial Interface"
         bps={bps} maxbps={maxbps} />
        <SbpTable msgs={SbpMsgTable}/>
      </div>
      </div>
    );
  }
}

export default App;
