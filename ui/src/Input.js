import React, { useState } from 'react';
import './Input.css'; // Import the CSS file for styling

const Input = () => {
  // State to store the audio file and dropdown selection
  const [audioFile, setAudioFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  
  // State to store the most recent input values
  const [recentInputs, setRecentInputs] = useState({
    audioFile: null,
    selectedOption: '',
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

  return (
    <div className="input-container">
      <h2 className="header-text">Input Audio and Select Instrument</h2>

      {/* Audio input */}
      <input
        type="file"
        accept="audio/*"
        onChange={handleAudioChange}
        className="audio-input"
      />
      {audioFile && <p className="file-info">Selected Audio: {audioFile.name}</p>}

      {/* Dropdown menu */}
      <select 
        onChange={handleOptionChange} 
        value={selectedOption} 
        className="dropdown-menu"
      >
        <option value="">Select an option</option>
        <option value="Option 1">Piano</option>
        <option value="Option 2">Harmonica</option>
        <option value="Option 3">Abhinav Vocals</option>
      </select>

      <div className="recent-inputs">
        <h3 className="recent-header">Recent Inputs:</h3>
        <p>Audio File: {recentInputs.audioFile ? recentInputs.audioFile.name : 'None'}</p>
        <p>Selected Option: {recentInputs.selectedOption || 'None'}</p>
      </div>
    </div>
  );
};

export default Input;
