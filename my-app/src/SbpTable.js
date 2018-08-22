import React, { Component } from 'react';
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
import {Table} from 'reactstrap'

import {SbpMsgDesc} from './SbpMsgDesc.js';
import {CommInterfaceHeader, CommInterfaceDetail} from './CommInterface.js';
import sbpIdTable from 'sbp';


console.log(sbpIdTable)

function getMsgInterfaceState(MsgId, interface_comma_setting, rate_type, soln_rate) {
  let msg_list = interface_comma_setting.split(",")
  let i = msg_list.index_of(MsgId)
  if (rate_type == 'soln') {
    if (i != -1) {
      let msg = msg_list[i]
      let divisor = 1
      let j = msg.index_of('/')
      if(j != -1) // there is a divisor other than 1
      {
        divisor = msg.split('/')[1]
      }
      return soln_rate / divisor
    }
  else {
    return "disabled"
  }
}
  return "Not determined by soln rate" 
}



let interfaces = [{name: "UART1", user_name: "Primary Serial Interface", 
                  desc: "UART1 is the primary serial interface for Piksi that is intended to provide navigation data to downstream systems over either lv-ttl or RS-232 Serial.  By default, it is configured to provide the messages that the Swift Console can display."},
                  {name: "UART0", user_name: "Secondary Serial Interface", 
                  desc: "UART0 is the secondary serial interface for Piksi that is intended to provide or receive corrections information. By default, it is configured to provide the messages required for piksi or Duro to act as a base station."}]

function testclick() {
  alert("clicked")
}

class SbpTable extends React.Component {



  tableList(msgs) {
  let return_list = []
  for(let msgidx in msgs)
  {
    for(let msgId in msgs[msgidx]) 
    {
      let msg = msgs[msgidx][msgId]
      return_list.push(<tr key={msgId}>
      <td><SbpMsgDesc msgName = {msg.msgName} shortDesc={msg.shortDesc} longDesc={msg.longDesc}/></td>
      <td>{msgId}</td>
      <td>{msg.msgLen}</td>
      {interfaces.map(function() {return (<td onClick={testclick}>disabled</td>)})}
    </tr>);
    console.log(msgs[msgidx][msgId].msgName);
  }
}
return return_list
}

  renderMsg(Msg, index, array) {
    console.log(array[index])
  return (
    <tr key={index}>
      <td><SbpMsgDesc msgName = {Msg.msgName} msgLen= {Msg.msgLen} msgDesc={Msg.shortDesc}/></td>
      <td>{Msg[index]}</td>
      {interfaces.map(function() {<td> "test" </td>})}
    </tr>
  )
}
  render() {
    let column_headers = [];
    for (let i = 0; i < interfaces.length; i++) {
      column_headers.push(<th className='w-10' key={i}>
                          <CommInterfaceHeader interfaceName={interfaces[i].name} 
                                       userFacingInterfaceName={interfaces[i].user_name}
                                       interfaceDesc={interfaces[i].desc}/>
                                       <CommInterfaceDetail interfaceName="UART1" userFacingInterfaceName="Primary Serial Interface"
         bps={30000} maxbps={115200} /></th>);
    }
    console.log(column_headers)
    let data = this.props.msgs
    return (
        <Table>
          <thead>
            <tr>
              <th className='w-25' >Message</th>
              <th className='w-2'>id</th>
              <th className='w-2'>len</th>
              {column_headers}
            </tr>
          </thead>
          <tbody>
            {this.tableList(this.props.msgs)}
          </tbody>
        </Table>
      
    );
  }
}

export {SbpTable}