import React, { useState } from 'react';
import './Output.css';

const Output = ({ fileId }) => {
  const [error, setError] = useState(null);

  // Function to handle the download of the PDF
  const handleDownload = async (fileType, fileName) => {
    const filePath = `/${fileName}`; // Path to the file in the public directory

    try {
      // Check if the file exists in the public directory
      const response = await fetch(filePath, { method: 'HEAD' });

      if (response.ok) {
        // File exists, trigger download
        const link = document.createElement('a');
        link.href = filePath;
        link.download = fileName;
        link.click();
      } else {
        // File doesn't exist
        setError(`${fileName} not found.`);
      }
    } catch (err) {
      // Handle error (e.g., network issues)
      setError('Error checking for file existence.');
    }
  };

  return (
    <div className="output-container">
      {/* Button for downloading PDF */}
      <button 
        onClick={() => handleDownload('pdf', 'sheet_music.pdf')} 
        className="download-button pdf-button"
      >
        Download PDF
      </button>

      {/* Button for downloading MIDI */}
      <button 
        onClick={() => handleDownload('midi', 'output.mid')} 
        className="download-button midi-button"
      >
        Download MIDI
      </button>

      {/* Display error message */}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Output;
