import React, { useState, useEffect } from 'react';
import './App.css';
const BACKEND_URL="http://127.0.0.1:8000/"
const DEFAULT_ALARM={
  schedule: ["30", "8", "*", "*", "*"],
  enabled: true,
}

function AlarmObj(id, schedule, enabled){
  return {
    id: id, 
    schedule: schedule,
    enabled: enabled
  }
}

async function sendRequest(route, method, body, setData){
  try {
    const response = await fetch(BACKEND_URL+route, {
      method: method,
      body: (body !== null)? JSON.stringify(body) : null,
      headers: {
        "Content-Type" : "application/json"
      }
    });
    if(response.status === 200){
      const result = await response.json();
      setData(result);
    }
    else{
      console.error("Error fetching data:", response);
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

async function updateAlarm(alarm, setState){
  await sendRequest("cron", "PUT", alarm, setState)
}

function EnableAlarm(props){
  return (
    <form>
      <input type="checkbox" defaultChecked={props.enabled} onChange={props.onChange}/>
    </form>
  )
}

function CreateAlarm(props){
  async function onClick(){
    // send a request
    sendRequest("cron", "POST", DEFAULT_ALARM, () => {});
    // update list of alarms by getting all alarms
    await sendRequest("crons", "GET", null, props.setData)
  }
  return (
    <button type="button" onClick={onClick}>Add new alarm</button>
  )
}

function Alarm(props){
  // const [enabled, setEnabled] = useState(props.enabled);
  const [state, setState] = useState(props.alarm)
  async function enabledChange(){
    // change enabled state of alarm
    updateAlarm({
      id: state.id,
      enabled: !state.enabled
    }, setState);
  }
  return (
    <div className="Alarm" key={"alarm" + props.id}>
      <p>id: {state.id}</p>
      <p>schedule: {state.schedule.join(" ")}</p>
      <EnableAlarm id={state.id} enabled={state.enabled} onChange={enabledChange}/>
    </div>
  )
}

function Alarms(props){
  return (
    <div>
      {
        props.alarms.map(alarm =>
          <Alarm key={alarm.id} alarm={alarm}/>
        )
      }
    </div>
  )
}

function App() {
  const [alarms, setAlarms] = useState([]);
  useEffect(() => {
    sendRequest("crons", "GET", null, setAlarms);
  }, []);

  return (
    <div className="App" key="app">
      <header className="App-header" key="header">
        ALARM CLOCKS
        <div>
          <Alarms alarms={alarms}/>
          <CreateAlarm setData={setAlarms}/>
        </div>
      </header>
    </div>
  );


}

export default App;
