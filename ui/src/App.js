import './App.css';
import Input from './Input';
import React from 'react';
import Output from './Output';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Input/>
        <Output audioFile = "ohio.mp3" pdfFile = "Amongus.pdf"/>
      </header>
    </div>
  );
}

export default App;
