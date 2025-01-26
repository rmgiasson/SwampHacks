import React, { useState, useRef } from 'react';
import './Output.css';
const Output = ({ audioFile, pdfFile }) => {

    return (
        <div className="output-container">
            <a href={audioFile} download>
                Download Audio File
            </a>
        </div>
      );
    };

export default Output;
