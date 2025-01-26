import React from 'react';
import './Output.css';

const Output = ({ audioFile, pdfFile, fileName }) => {
  const handleDownload = (type) => {
    // Use the public URL for files in the React public folder
    const url = `http://localhost:3000/${fileName}`;  // Serve from public/ folder
    window.location.href = type === 'pdf' ? `${url}.pdf` : `${url}.wav`;
  };

  return (
    <div className="output-container">
      <button onClick={() => handleDownload('pdf')} className="download-button">
        Download PDF
      </button>
      <button onClick={() => handleDownload('wav')} className="download-button">
        Download WAV
      </button>
    </div>
  );
};

export default Output;
