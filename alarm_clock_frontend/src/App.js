import React, { useState, useEffect } from 'react';
import './App.css';
const BACKEND_URL="http://127.0.0.1:8000/"
const DEFAULT_ALARM={
  schedule: ["30", "8", "*", "*", "*"],
  enabled: true,
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
      return response.status;
    }
    else{
      console.error("Error fetching data:", response);
      return response.status;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    return -1;
  }
};

async function updateAlarm(alarm, setState){
  let resp_code = await sendRequest("cron", "PUT", alarm, setState);
  console.log("RESPONSE CODE", resp_code)
  if(resp_code !== 200){
    await sendRequest("cron?id="+alarm.id, "GET", null, setState);
  }
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

function EditingControls(props){

  function cancelEditing(){
    props.setEditingMode(false);
  }
  function submitEdit(){
    props.setEditingMode(false);
    props.submitChanges()
  }

  return (
    <div>
      <button key={"cancel-edit_"+props.state.id} type="button" onClick={cancelEditing}>Cancel Editing</button>
      <button key={"submit-edit_"+props.state.id} type="button" onClick={submitEdit}>Submit changes</button>
    </div>
  )
}

function Schedule(props){
  if(!props.editingMode){
    return (
      <p>{props.schedule.join(" ")}</p>
    )
  }
  else{
    function updateSchedule(e, index){
      // copy props schedule
      let schedule = [...props.schedule];
      // update with new value
      schedule[index] = e.target.value;
      // set in parent
      props.setSchedule(schedule);
    }
    return (
      <form>
        {props.schedule.map((sched, index) => {
          const onChange = (e, index) => updateSchedule(e);
          return <input key={index} type="text" defaultValue={sched} onChange={(e) => updateSchedule(e, index)}></input>;
        })}
      </form>
    )
  }
}
    // change enabled state of alarm

function Alarm(props){
  const [state, setState] = useState(props.alarm)
  const [editingMode, setEditingMode] = useState(false);
  async function setSchedule(schedule){
    setState({
      ...state,
      schedule: schedule
    })
  }
  async function enabledChange(){
    setState({
      ...state,
      enabled: !state.enabled
    });
  }
  async function submitChanges(){
    updateAlarm(state, setState);
  }
  function editingChange(){
    setEditingMode(!editingMode);
  }

  function submitEdit(){
    console.log("editing finished, need to update state:", state);
  }

  const editButton = <input key={"edit_"+state.id}type="checkbox" defaultChecked={editingMode} onChange={editingChange}/>
  const editControls = <EditingControls state={state} setEditingMode={setEditingMode} submitChanges={submitChanges}/>
  return (
    <div className="Alarm" key={"alarm_" + props.id}>
      <p>id: {state.id}</p>
      <Schedule schedule={state.schedule} editingMode={editingMode} setSchedule={setSchedule}/>
      <p>is enabled: {state.enabled.toString()}</p>
      <form>
        {/* enable/disable alarm */}
        {editingMode? <input type="checkbox" defaultChecked={state.enabled} onChange={enabledChange}/> : null}
        {editingMode? editControls : editButton}
        <p>IN EDITING MODE: {editingMode.toString()}</p>
      </form>
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
