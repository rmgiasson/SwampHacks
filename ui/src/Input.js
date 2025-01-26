import React, { useState } from 'react';
import './Input.css'; // Import the CSS file for styling

const Input = () => {
  // State to store the audio file and dropdown selection
  const [audioFile, setAudioFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [selectedKey, setSelectedKey] = useState('');
  
  // State to store the most recent input values
  const [recentInputs, setRecentInputs] = useState({
    audioFile: null,
    selectedOption: '',
    selectedKey: '',
  });

  // Handle audio file change
  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
      setRecentInputs((prevState) => ({
        ...prevState,
        audioFile: file,
      }));
    }
  };

  // Handle dropdown option change
  const handleOptionChange = (e) => {
    const option = e.target.value;
    setSelectedOption(option);
    setRecentInputs((prevState) => ({
      ...prevState,
      selectedOption: option,
    }));
  };

  const handleKeyChange = (e) => {
    const option = e.target.value;
    setSelectedKey(option);
    setRecentInputs((prevState) => ({
      ...prevState,
      selectedKey: option,
    }));
  };

  const handleButtonClick = () => {
    // Log the current values of the selected audio file and dropdown option
    console.log('Button Clicked!');
    console.log('Selected Audio File:', audioFile ? audioFile.name : 'None');
    console.log('Selected Option:', selectedOption || 'None');
  };

  return (
    <div className="input-container">
      <h2 className="header-text">Audio selection</h2>

      {/* Dropdown menu */}
      <select 
        onChange={handleOptionChange} 
        value={selectedOption} 
        className="dropdown-menu"
      >
        <option value="">Select an instrument</option>
        <option value="Option 1">Piano</option>
        <option value="Option 2">Harmonica</option>
        <option value="Option 3">Abhinav Vocals</option>
      </select>

      {/* Dropdown menu */}
      <select 
        onChange={handleKeyChange} 
        value={selectedKey} 
        className="dropdown-menu"
      >
        <option value="">Select a key</option>
        <option value="Option 0">Original Key</option>
        <option value="Option 1">C</option>
        <option value="Option 2">C#</option>
        <option value="Option 3">D</option>
        <option value="Option 4">Eb</option>
        <option value="Option 5">E</option>
        <option value="Option 6">F</option>
        <option value="Option 7">F#</option>
        <option value="Option 8">G</option>
        <option value="Option 9">G#</option>
        <option value="Option 10">A</option>
        <option value="Option 11">Bb</option>
        <option value="Option 12">B</option>
      </select>

      {/* Audio input */}
      <input
        type="file"
        accept="audio/*"
        onChange={handleAudioChange}
        className="audio-input"
      />
      {audioFile && <p className="file-info">Selected Audio: {audioFile.name}</p>}

      

      <button onClick={handleButtonClick} className="action-button">
        Submit
      </button>

    </div>
  );
};

export default Input;
