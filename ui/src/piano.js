import React, { useState, useEffect } from 'react';
import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';
import MidiPlayer from 'midi-player-js';
import * as Tone from 'tone';

const TwoOctaveKeyboard = () => {
  const firstNote = MidiNumbers.fromNote('C2'); // Start from middle C
  const lastNote = MidiNumbers.fromNote('B6'); // Two octaves up
  const keyboardShortcuts = KeyboardShortcuts.create({
    firstNote,
    lastNote,
    keyboardConfig: KeyboardShortcuts.HOME_ROW,
  });

  const [activeNotes, setActiveNotes] = useState([]); // Highlighted keys
  const [player, setPlayer] = useState(null); // MIDI player instance
  const [synth, setSynth] = useState(null); // Synth instance

  useEffect(() => {
    // Initialize a Tone.js synthesizer
    const newSynth = new Tone.PolySynth().toDestination();
    setSynth(newSynth);

    // Initialize MIDI Player
    const midiPlayer = new MidiPlayer.Player((event) => {
      if (event.name === 'Note on') {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        setActiveNotes((prev) => [...prev, midiNumber]); // Highlight key
        newSynth.triggerAttack(note); // Play note
      }

      if (event.name === 'Note off') {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        setActiveNotes((prev) => prev.filter((n) => n !== midiNumber)); // Remove highlight
        newSynth.triggerRelease(note);
      }
    });

    setPlayer(midiPlayer);

    // Clean up player on unmount
    return () => {
      midiPlayer.stop();
      newSynth.dispose();
    };
  }, []);

  const loadAndPlayMIDI = (file) => {
    if (!player) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const arrayBuffer = e.target.result;
      player.loadArrayBuffer(arrayBuffer);
      player.play();
    };
    reader.readAsArrayBuffer(file);
  };

  const pausePlayback = () => {
    if (player) {
      player.pause();

      // Stop all currently playing notes
      synth.releaseAll(); // Clear all active notes on the synthesizer
      setActiveNotes([]); // Clear highlighted keys
    }
  };

  const stopPlayback = () => {
    if (player) {
      player.stop();

      // Stop all currently playing notes
      synth.releaseAll(); // Clear all active notes on the synthesizer
      setActiveNotes([]); // Clear highlighted keys
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <input
        type="file"
        accept=".mid"
        onChange={(e) => loadAndPlayMIDI(e.target.files[0])}
        style={{ marginBottom: '20px' }}
      />
      <Piano
        noteRange={{ first: firstNote, last: lastNote }}
        width={1200}
        playNote={(midiNumber) => setActiveNotes((prev) => [...prev, midiNumber])}
        stopNote={(midiNumber) => setActiveNotes((prev) => prev.filter((n) => n !== midiNumber))}
        activeNotes={activeNotes}
        keyboardShortcuts={keyboardShortcuts}
      />
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button onClick={() => player?.play()}>Play</button>
        <button onClick={() => pausePlayback()}>Pause</button>
        <button onClick={() => stopPlayback()}>Stop</button>
      </div>
    </div>
  );
};

export default TwoOctaveKeyboard;