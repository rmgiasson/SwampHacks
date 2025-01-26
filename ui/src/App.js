import './App.css';
import Input from './Input';
import React, { useState, useEffect } from 'react';
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
  const [midiFileUrl, setMidiFileUrl] = useState(null); // State for MIDI file URL

  // Toggle Piano visibility
  const togglePiano = () => {
    setIsPianoVisible(!isPianoVisible);
  };

  // Check if the sheet_music.pdf file exists and update the state
  useEffect(() => {
    const checkPdfFile = async () => {
      try {
        const response = await fetch('/sheet_music.pdf');
        if (response.ok) {
          setPdfFileUrl('/sheet_music.pdf');
        } else {
          setPdfFileUrl(null);
        }
      } catch (error) {
        setPdfFileUrl(null);
        console.error('Error checking for sheet_music.pdf:', error);
      }
    };

    checkPdfFile();
  }, []);

  // Check if the output.midi file exists and update the state
  useEffect(() => {
    const checkMidiFile = async () => {
      try {
        const response = await fetch('/output.midi');
        if (response.ok) {
          setMidiFileUrl('/output.midi');
        } else {
          setMidiFileUrl(null);
        }
      } catch (error) {
        setMidiFileUrl(null);
        console.error('Error checking for output.midi:', error);
      }
    };

    checkMidiFile();
  }, []);

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
          <Output fileId={fileId} />
        </div>
        <div className="App-header2">
          <button onClick={togglePiano} className="toggle-piano-button">
            {isPianoVisible ? 'Hide Piano' : 'Show Piano'}
          </button>
          {isPianoVisible && <Piano midiFileUrl={midiFileUrl} />}
        </div>
      </header>

      {/* Allow users to download PDF and WAV files dynamically */}
      <div className="file-links">
        {pdfFileUrl ? (
          <div>
            <h3>PDF</h3>
            <a href={pdfFileUrl} download={`sheet_music.pdf`}>
              Download PDF
            </a>
          </div>
        ) : (
          <p>No PDF to display. Submit a file to generate the sheet music.</p>
        )}
      </div>
    </div>
  );
}

export default App;
