import React from 'react';
import './Output.css';

const Output = ({ fileId }) => {
  return (
    <div className="output-container">
      <button onClick={() => handleDownload('pdf')} className="download-button">
        Download PDF
      </button>
    </div>
  );
};

export default Output;
