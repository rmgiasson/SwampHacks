import './App.css';
import Input from './Input';
import React, { useState } from 'react';
import Output from './Output';
import Piano from './piano';
import { Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

function App() {
  const [isPianoVisible, setIsPianoVisible] = useState(true);
  const [pdfFileUrl, setPdfFileUrl] = useState(null); // State for PDF file URL

  // Toggle Piano visibility
  const togglePiano = () => {
    setIsPianoVisible(!isPianoVisible);
  };

  // Function to handle file submission and update the PDF file URL
  const handleFileSubmission = async (file, instrument) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('instrument', instrument);

      // POST request to upload the file
      const response = await fetch('http://localhost:3001/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      // Assuming the backend returns the filename or identifier
      const { message } = await response.json();

      // Generate the URL for the PDF
      const pdfUrl = `http://localhost:3000/${message}.pdf`;  // Serve from public/ folder

      // Update the state with the new PDF URL
      setPdfFileUrl(pdfUrl);
    } catch (error) {
      console.error('Error during file submission:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-header1">
          {/* Pass handleFileSubmission to Input */}
          <Input onSubmit={handleFileSubmission} />
          <div className="pdf-viewer-container">
            {pdfFileUrl ? (
              <Viewer fileUrl={pdfFileUrl} />
            ) : (
              <p>No PDF to display. Submit a file to generate the sheet music.</p>
            )}
          </div>
          <Output fileName="star" />
        </div>
        <div className="App-header2">
          <button onClick={togglePiano} className="toggle-piano-button">
            {isPianoVisible ? 'Hide Piano' : 'Show Piano'}
          </button>
          {isPianoVisible && <Piano />}
        </div>
      </header>
    </div>
  );
}

export default App;
