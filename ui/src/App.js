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
  const [pdfFileUrl, setPdfFileUrl] = useState(null); 
  const [midiFileUrl, setMidiFileUrl] = useState(null); 
  const [lastModifiedTime, setLastModifiedTime] = useState(null);
  const togglePiano = () => {
    setIsPianoVisible(!isPianoVisible);
  };

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

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch('/output.mid', { method: 'HEAD' });
        if (response.ok) {
          const newModifiedTime = response.headers.get('last-modified');
          if (newModifiedTime && newModifiedTime !== lastModifiedTime) {
            setLastModifiedTime(newModifiedTime);
            setMidiFileUrl('/output.mid');
          }
        } else {
          setMidiFileUrl(null);
        }
      } catch (error) {
        setMidiFileUrl(null);
        console.error('Error checking for output.mid:', error);
      }
    }, 5000); 

    return () => clearInterval(interval);
  }, [lastModifiedTime]);

  const handleFileSubmission = async (file, instrument) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('instrument', instrument);

      const response = await fetch('http://127.0.0.1:8000/api/upload/', {
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
          <Input onSubmit={handleFileSubmission} />
          <div className="pdf-viewer-container">
            {pdfFileUrl ? (
              <Viewer fileUrl={pdfFileUrl} />
            ) : (
              <p>No PDF to display. Submit a file to generate the sheet music.</p>
            )}
          </div>
          <Output />
        </div>
        <div className="App-header2">
          <button onClick={togglePiano} className="toggle-piano-button">
            {isPianoVisible ? 'Hide Piano' : 'Show Piano'}
          </button>
          {isPianoVisible && <Piano midiFileUrl={midiFileUrl} />}
        </div>
      </header>
    </div>
  );
}

export default App;
