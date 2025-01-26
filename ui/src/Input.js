import React, { useState } from 'react';
import './Input.css';

const Input = ({ onSubmit }) => {
  const [audioFile, setAudioFile] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    setAudioFile(file);
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleSubmit = () => {
    if (audioFile && selectedOption) {
      onSubmit(audioFile, selectedOption); // Pass file and instrument to App
    } else {
      alert('Please select a file and instrument!');
    }
  };

  return (
    <div className="input-container">
      <h2 className="header-text">Audio Selection</h2>
      <select
        onChange={handleOptionChange}
        value={selectedOption}
        className="dropdown-menu"
      >
        <option value="">Select an instrument</option>
        <option value="piano">Piano</option>
        <option value="harmonica">Harmonica</option>
      </select>
      <input
        type="file"
        accept="audio/*"
        onChange={handleAudioChange}
        className="audio-input"
      />
      <button onClick={handleSubmit} className="action-button">
        Submit
      </button>
    </div>
  );
};

export default Input;
