import './App.css';
import Input from './Input';
import React, { useState } from 'react';
import Output from './Output';
import Piano from'./piano';

function App() {
  const [isPianoVisible, setIsPianoVisible] = useState(true);

  // Function to toggle the visibility of the Piano component
  const togglePiano = () => {
    setIsPianoVisible(!isPianoVisible);
  };
  
  return (
    <div className="App">
      <header className="App-header">
        <div className="App-header1">
          <Input/>
          <Output audioFile = "ohio.mp3" pdfFile = "Amongus.pdf"/>
        </div>
        <div className="App-header2">
          <button onClick={togglePiano}>
            {isPianoVisible ? 'Hide Piano' : 'Show Piano'}
          </button>
          {isPianoVisible && <Piano />}
        </div>
      </header>
    </div>
  );
}

export default App;
