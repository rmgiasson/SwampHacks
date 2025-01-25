import React from 'react';
import './Output.css';

const Output = ({ audioFile, pdfFile }) => {
  return (
    <div className="output-container">
      <h2>Audio & PDF Display</h2>

      {/* Check if audio file is provided */}
      {audioFile && (
        <div className="audio-player">
          <h3>Audio Player:</h3>
          <audio controls>
            <source src={audioFile} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

      {/* Check if PDF file is provided */}
      {pdfFile && (
        <div className="pdf-viewer">
          <h3>PDF Viewer:</h3>
          <embed src={pdfFile} width="100%" height="500px" type="application/pdf" />
        </div>
      )}
    </div>
  );
};

export default Output;
