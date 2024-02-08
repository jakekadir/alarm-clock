import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL="http://127.0.0.1:8000/"

function Alarm(props){
  console.log("id", props.id);
  return (
    <div className="Alarm" key={props.id}>
      <p>id: {props.id}</p>
      <p>schedule: {props.schedule.join(" ")}</p>
    </div>
  )
}

const Alarms = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(BACKEND_URL+"crons");
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {data.map(alarm => {
        return(
          <Alarm key={alarm.id} id={alarm.id} schedule={alarm.schedule}/>
        );
      })}
    </div>
  )
}

function App() {
  return (
    <div className="App" key="app">
      <header className="App-header" key="header">
        <Alarms/>
      </header>
    </div>
  );

}

export default App;
