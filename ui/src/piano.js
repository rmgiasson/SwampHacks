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
  const [isPlaying, setIsPlaying] = useState(false); // Track playback state

  useEffect(() => {
    // Initialize a Tone.js synthesizer
    const newSynth = new Tone.PolySynth(Tone.Synth, {
      oscillator: { type: 'triangle' },
      envelope: {
        attack: 0.02,
        decay: 0.2,
        sustain: 0.5,
        release: 0.3,
      },
    }).toDestination();
    setSynth(newSynth);

    // Initialize MIDI Player
    const midiPlayer = new MidiPlayer.Player((event) => {
      console.log('MIDI Event:', event); // Debugging: Log all MIDI events

      if (event.name === 'Note on' && event.velocity > 0) {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        if (!activeNotes.includes(midiNumber)) {
          setActiveNotes((prev) => [...prev, midiNumber]); // Highlight key
          newSynth.triggerAttack(note); // Play note
          console.log(`Playing Note On: ${note}`);
        }
      }

      if (event.name === 'Note off' || (event.name === 'Note on' && event.velocity === 0)) {
        const midiNumber = event.noteNumber;
        const note = Tone.Frequency(midiNumber, 'midi').toNote();
        setActiveNotes((prev) => prev.filter((n) => n !== midiNumber)); // Remove highlight
        newSynth.triggerRelease(note); // Ensure note is released properly
        console.log(`Releasing Note Off: ${note}`);
      }
    });

    // Detect when the player finishes playing
    midiPlayer.on('endOfFile', () => {
      setIsPlaying(false); // Reset the play button highlight
      console.log('Playback finished');
    });

    setPlayer(midiPlayer);

    // Clean up player and synth on unmount
    return () => {
      midiPlayer.stop();
      newSynth.dispose();
    };
  }, []);

  const loadAndPlayMIDI = (file) => {
    if (!player || !synth) return;

    console.log(`Loading MIDI File: ${file.name}`);

    // Stop and reset the previous playback
    if (player) {
      player.stop(); // Stop any existing playback
    }
    if (synth) {
      synth.releaseAll(); // Release all active notes
    }
    setActiveNotes([]); // Reset highlighted notes
    setIsPlaying(false); // Reset playback state

    // Read and load the new MIDI file
    const reader = new FileReader();
    reader.onload = (e) => {
      const arrayBuffer = e.target.result;
      player.loadArrayBuffer(arrayBuffer);
      console.log('MIDI File Loaded Successfully');
      player.play(); // Automatically start playing the new file
      setIsPlaying(true); // Highlight the play button
    };
    reader.readAsArrayBuffer(file);
  };

  const playPlayback = async () => {
    // Ensure the audio context is running
    if (Tone.context.state !== 'running') {
      await Tone.start();
      console.log('Audio context started');
    }

    if (player && !player.isPlaying()) {
      player.play();
      console.log('Playback started');
      setIsPlaying(true); // Highlight the Play button
    }
  };

  const pausePlayback = () => {
    if (player && player.isPlaying()) {
      player.pause();
      setIsPlaying(false); // Unhighlight the Play button
      console.log('Playback paused');

      // Stop all currently playing notes
      synth.releaseAll(); // Clear all active notes on the synthesizer
      setActiveNotes([]); // Clear highlighted keys
    }
  };

  const stopPlayback = () => {
    if (player) {
      player.stop();
      setIsPlaying(false); // Unhighlight the Play button
      console.log('Playback stopped');

      // Stop all currently playing notes
      synth.releaseAll(); // Clear all active notes on the synthesizer
      setActiveNotes([]);
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
        <button
          onClick={() => playPlayback()}
          style={{
            backgroundColor: isPlaying ? '#4CAF50' : '#61dafb',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginRight: '10px',
          }}
        >
          Play
        </button>
        <button
          onClick={() => pausePlayback()}
          style={{
            backgroundColor: '#f0ad4e',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginRight: '10px',
          }}
        >
          Pause
        </button>
        <button
          onClick={() => stopPlayback()}
          style={{
            backgroundColor: '#d9534f',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Stop
        </button>
      </div>
    </div>
  );
};

export default TwoOctaveKeyboard;