import React, { useState } from 'react';
import './Output.css';

const Output = ({ fileId }) => {
  const [error, setError] = useState(null);

  const handleDownload = async (fileType, fileName) => {
    const filePath = `/${fileName}`; 

    try {
      const response = await fetch(filePath, { method: 'HEAD' });

      if (response.ok) {
        const link = document.createElement('a');
        link.href = filePath;
        link.download = fileName;
        link.click();
      } else {
        setError(`${fileName} not found.`);
      }
    } catch (err) {
      setError('Error checking for file existence.');
    }
  };

  return (
    <div className="output-container">
      <button 
        onClick={() => handleDownload('pdf', 'sheet_music.pdf')} 
        className="download-button pdf-button"
      >
        Download PDF
      </button>

      <button 
        onClick={() => handleDownload('midi', 'output.mid')} 
        className="download-button midi-button"
      >
        Download MIDI
      </button>

      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Output;
