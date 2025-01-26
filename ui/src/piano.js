import React, { useState, useEffect } from 'react';
import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';
import MidiPlayer from 'midi-player-js';
import * as Tone from 'tone';

const TwoOctaveKeyboard = ({ midiFileUrl }) => {
  const firstNote = MidiNumbers.fromNote('C2'); // Start from middle C
  const lastNote = MidiNumbers.fromNote('B6'); // Two octaves up
  const keyboardShortcuts = KeyboardShortcuts.create({
    firstNote,
    lastNote,
    keyboardConfig: KeyboardShortcuts.HOME_ROW,
  });

  const [activeNotes, setActiveNotes] = useState([]);
  const [player, setPlayer] = useState(null);
  const [synth, setSynth] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Initialize a Tone.js synthesizer
    const newSynth = new Tone.PolySynth(Tone.Synth, {
      oscillator: { type: 'triangle' },
      envelope: {
        attack: 0.02,
        decay: 0.2,
        sustain: 0.3,
        release: 0.1, // Short release time for quick note-off behavior
      },
    }).toDestination();
    setSynth(newSynth);

    const midiPlayer = new MidiPlayer.Player((event) => {
      if (event.name === 'Note on' && event.velocity > 0) {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        if (!activeNotes.includes(midiNumber)) {
          setActiveNotes((prev) => [...prev, midiNumber]);
          newSynth.triggerAttack(note); // Play the note
        }
      }
      if (event.name === 'Note off' || (event.name === 'Note on' && event.velocity === 0)) {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        setActiveNotes((prev) => prev.filter((n) => n !== midiNumber));
        newSynth.triggerRelease(note); // Release the note quickly
      }
    });

    midiPlayer.on('endOfFile', () => setIsPlaying(false));
    setPlayer(midiPlayer);

    return () => {
      midiPlayer.stop();
      newSynth.dispose();
    };
  }, []);

  useEffect(() => {
    const fetchAndPlayMidi = async () => {
      if (midiFileUrl && player) {
        const response = await fetch(midiFileUrl);
        const arrayBuffer = await response.arrayBuffer();
        player.loadArrayBuffer(arrayBuffer);
        player.play();
        setIsPlaying(true);
      }
    };

    fetchAndPlayMidi();
  }, [midiFileUrl, player]);

  const restartPlayback = () => {
    if (player) {
      player.stop();
      player.play();
      setIsPlaying(true);
    }
  };

  const pauseOrResumePlayback = () => {
    if (player) {
      if (player.isPlaying()) {
        player.pause();
        setIsPlaying(false);
        synth.releaseAll(); 
      } else {
        player.play();
        setIsPlaying(true);
      }
    }
  };
  

  return (
    <div style={{ padding: '20px' }}>
      <Piano
        noteRange={{ first: firstNote, last: lastNote }}
        width={1200}
        playNote={(midiNumber) => setActiveNotes((prev) => [...prev, midiNumber])}
        stopNote={(midiNumber) => setActiveNotes((prev) => prev.filter((n) => n !== midiNumber))}
        activeNotes={activeNotes}
        keyboardShortcuts={keyboardShortcuts}
      />
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button onClick={restartPlayback} style={buttonStyle}>
          Restart
        </button>
        <button onClick={pauseOrResumePlayback} style={buttonStyle}>
          {isPlaying ? 'Pause' : 'Resume'}
        </button>
      </div>
    </div>
  );
};

const buttonStyle = {
  backgroundColor: '#00bcd4',
  color: 'white',
  padding: '10px 20px',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  marginRight: '10px',
};

export default TwoOctaveKeyboard;
