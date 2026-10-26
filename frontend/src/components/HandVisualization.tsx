import React from 'react';
import type { ControllerState } from '../types';

interface HandVisualizationProps {
  gripState: string;
  controllerState: ControllerState;
}

export const HandVisualization: React.FC<HandVisualizationProps> = ({
  gripState,
  controllerState,
}) => {
  const {
    current_pressure_n,
    grip_force_percent,
    contact_detected,
    slip_detected,
    controller_action,
  } = controllerState;

  // Normalized flexion factor: 0.0 (fully open) to 1.0 (fully flexed)
  const flexion = Math.min(1.0, Math.max(0.0, grip_force_percent / 100));

  // Joint rotation angles based on grip type & flexion
  let thumbAngle = 0;
  let indexCurl = 0;
  let middleCurl = 0;
  let ringCurl = 0;
  let pinkyCurl = 0;

  const stateKey = gripState.toUpperCase().replace(' ', '_');

  if (stateKey === 'POWER_GRIP') {
    thumbAngle = 20 + flexion * 50;
    indexCurl = flexion * 68;
    middleCurl = flexion * 72;
    ringCurl = flexion * 70;
    pinkyCurl = flexion * 65;
  } else if (stateKey === 'PINCH_GRIP') {
    thumbAngle = 28 + flexion * 42;
    indexCurl = flexion * 62;
    middleCurl = flexion * 28;
    ringCurl = flexion * 22;
    pinkyCurl = flexion * 18;
  } else if (stateKey === 'RELEASE' || stateKey === 'OPEN') {
    thumbAngle = Math.max(0, 8 * flexion);
    indexCurl = Math.max(0, 4 * flexion);
    middleCurl = Math.max(0, 4 * flexion);
    ringCurl = Math.max(0, 4 * flexion);
    pinkyCurl = Math.max(0, 4 * flexion);
  }

  // FSR pressure color & halo
  const getSensorColor = () => {
    if (slip_detected) return '#ef4444'; // Red alert on slip
    if (!contact_detected) return '#3b4252'; // Muted dark inactive
    if (current_pressure_n > 65) return '#f59e0b'; // Amber near safety ceiling
    return '#22c55e'; // High-contrast green stable contact
  };

  const padColor = getSensorColor();

  return (
    <div className="bg-background-surface border border-border rounded-md p-4 flex flex-col justify-between relative shadow-sm h-full">
      {/* Hand Status Overlay Bar */}
      <div className="w-full flex items-center justify-between border-b border-border-subtle pb-2 mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono uppercase tracking-wider text-foreground font-semibold">
            Articulated Bionic Hand
          </span>
          <span className="text-[10px] bg-background-elevated border border-border-strong px-2 py-0.5 rounded text-foreground font-mono">
            5-DOF Virtual Kinematics
          </span>
        </div>
        <div className="flex items-center space-x-3 text-xs font-mono">
          <span className="text-foreground-secondary">
            Servo Effort: <span className="text-foreground font-bold">{grip_force_percent.toFixed(0)}%</span>
          </span>
          <span className="text-foreground-secondary">
            State: <span className="text-foreground font-bold">{controller_action}</span>
          </span>
        </div>
      </div>

      {/* SVG Prosthetic Hand Canvas - Tightened ViewBox to Eliminate Empty Margins */}
      <div className="relative w-full flex-1 flex items-center justify-center min-h-[340px] bg-background-subtle/50 rounded border border-border-subtle overflow-hidden">
        <svg
          viewBox="90 55 235 325"
          preserveAspectRatio="xMidYMid meet"
          className="w-full h-full max-h-[350px] select-none"
          style={{ transition: 'all 0.15s ease-out' }}
        >
          <defs>
            {/* Technical grid backdrop */}
            <pattern id="handGrid" width="16" height="16" patternUnits="userSpaceOnUse">
              <path d="M 16 0 L 0 0 0 16" fill="none" stroke="#1c202a" strokeWidth="0.8" />
            </pattern>
          </defs>
          <rect x="90" y="55" width="235" height="325" fill="url(#handGrid)" opacity="0.65" />

          {/* Wrist / Forearm Chassis Mounting */}
          <path
            d="M 165 330 L 255 330 L 265 375 L 155 375 Z"
            fill="#1e232e"
            stroke="#546077"
            strokeWidth="2.5"
          />
          {/* Main wrist pivot hub */}
          <circle cx="210" cy="332" r="15" fill="#29303d" stroke="#687691" strokeWidth="2.5" />
          <circle cx="210" cy="332" r="6" fill="#14171d" stroke="#546077" strokeWidth="1.5" />
          <line x1="192" y1="332" x2="228" y2="332" stroke="#8896b0" strokeWidth="2" strokeDasharray="3 2" />

          {/* Palm Structural Body - High-Contrast Armor */}
          <polygon
            points="138,242 158,168 262,168 282,242 254,324 166,324"
            fill="#232834"
            stroke="#687691"
            strokeWidth="3"
          />
          {/* Palm Inner Skeleton Inset */}
          <polygon
            points="160,182 260,182 268,236 244,300 176,300 152,236"
            fill="#181c24"
            stroke="#3d4659"
            strokeWidth="2"
          />

          {/* Palm Tactile FSR Sensor Pad */}
          <g transform="translate(210, 245)">
            {contact_detected && (
              <circle
                cx="0"
                cy="0"
                r="18"
                fill="none"
                stroke={padColor}
                strokeWidth="1.5"
                opacity="0.75"
                strokeDasharray="3 3"
              />
            )}
            <circle
              cx="0"
              cy="0"
              r="12"
              fill={padColor}
              opacity={contact_detected ? 1.0 : 0.4}
              stroke="#687691"
              strokeWidth="2"
            />
            <text
              x="0"
              y="3"
              textAnchor="middle"
              fontSize="7"
              fontFamily="monospace"
              fill="#0e1014"
              fontWeight="bold"
            >
              FSR-P
            </text>
          </g>

          {/* Grasped Object in Power Grip mode */}
          {stateKey === 'POWER_GRIP' && flexion > 0.25 && (
            <g opacity={Math.min(1, flexion * 1.5)}>
              <rect
                x="170"
                y="125"
                width="78"
                height="120"
                rx="14"
                fill="#2e3543"
                stroke="#94a3b8"
                strokeWidth="2.5"
              />
              <line x1="180" y1="145" x2="238" y2="145" stroke="#64748b" strokeWidth="2.5" />
              <line x1="180" y1="225" x2="238" y2="225" stroke="#64748b" strokeWidth="2.5" />
              <text
                x="209"
                y="188"
                textAnchor="middle"
                fontSize="10"
                fontFamily="monospace"
                fontWeight="bold"
                fill="#e2e8f0"
                letterSpacing="1"
              >
                PAYLOAD
              </text>
            </g>
          )}

          {/* Grasped Object in Pinch Grip mode */}
          {stateKey === 'PINCH_GRIP' && flexion > 0.25 && (
            <g opacity={Math.min(1, flexion * 1.5)}>
              <rect
                x="158"
                y="122"
                width="32"
                height="32"
                rx="5"
                fill="#363f50"
                stroke="#a6b3c7"
                strokeWidth="2.5"
              />
              <circle cx="174" cy="138" r="4.5" fill="#5a6880" />
              <text
                x="174"
                y="141"
                textAnchor="middle"
                fontSize="7"
                fontFamily="monospace"
                fontWeight="bold"
                fill="#f1f5f9"
              >
                PEG
              </text>
            </g>
          )}

          {/* THUMB (Digit 1) */}
          <g
            transform={`translate(144, 254) rotate(${-thumbAngle})`}
            style={{ transition: 'transform 0.15s ease-out' }}
          >
            {/* Metacarpal Joint Pivot */}
            <circle cx="0" cy="0" r="10" fill="#2d3545" stroke="#687691" strokeWidth="2.5" />
            <circle cx="0" cy="0" r="4" fill="#181c24" stroke="#485368" strokeWidth="1.5" />
            {/* Proximal Bone */}
            <rect x="-9" y="-36" width="18" height="36" rx="5" fill="#262d3a" stroke="#54627b" strokeWidth="2" />

            {/* Tendon wire along thumb */}
            <line
              x1="0"
              y1="0"
              x2="0"
              y2="-36"
              stroke="#94a3b8"
              strokeWidth="1.5"
              strokeDasharray="2 2"
              opacity={0.5 + flexion * 0.5}
            />

            {/* Distal Joint */}
            <g
              transform={`translate(0, -36) rotate(${-thumbAngle * 0.75})`}
              style={{ transition: 'transform 0.15s ease-out' }}
            >
              <circle cx="0" cy="0" r="8" fill="#323c4d" stroke="#6d7b97" strokeWidth="2" />
              <path
                d="M -8 0 L -7 -34 C -7 -40 7 -40 7 -34 L 8 0 Z"
                fill="#2c3444"
                stroke="#5d6c88"
                strokeWidth="2"
              />
              {/* Thumb FSR Sensor with active halo */}
              {contact_detected && (
                <circle
                  cx="0"
                  cy="-30"
                  r="11"
                  fill="none"
                  stroke={padColor}
                  strokeWidth="1.5"
                  opacity="0.8"
                  strokeDasharray="2 2"
                />
              )}
              <circle
                cx="0"
                cy="-30"
                r="6.5"
                fill={padColor}
                opacity={contact_detected ? 1.0 : 0.45}
                stroke="#687691"
                strokeWidth="1.5"
              />
            </g>
          </g>

          {/* INDEX FINGER (Digit 2) */}
          <g
            transform={`translate(174, 168) rotate(${indexCurl * 0.42})`}
            style={{ transition: 'transform 0.15s ease-out' }}
          >
            <circle cx="0" cy="0" r="9.5" fill="#2d3545" stroke="#687691" strokeWidth="2.5" />
            <circle cx="0" cy="0" r="3.5" fill="#181c24" />
            <rect x="-8" y="-40" width="16" height="40" rx="5" fill="#262d3a" stroke="#54627b" strokeWidth="2" />

            {/* Intermediate Phalanx */}
            <g
              transform={`translate(0, -40) rotate(${indexCurl * 0.52})`}
              style={{ transition: 'transform 0.15s ease-out' }}
            >
              <circle cx="0" cy="0" r="7.5" fill="#323c4d" stroke="#6d7b97" strokeWidth="2" />
              <rect x="-7" y="-34" width="14" height="34" rx="4" fill="#2b3342" stroke="#5d6c88" strokeWidth="2" />

              {/* Distal Phalanx + FSR */}
              <g
                transform={`translate(0, -34) rotate(${indexCurl * 0.52})`}
                style={{ transition: 'transform 0.15s ease-out' }}
              >
                <circle cx="0" cy="0" r="6" fill="#364052" stroke="#7584a2" strokeWidth="2" />
                <path d="M -6 0 L -5 -26 C -5 -32 5 -32 5 -26 L 6 0 Z" fill="#303848" stroke="#637391" strokeWidth="2" />
                {contact_detected && (
                  <circle
                    cx="0"
                    cy="-22"
                    r="10"
                    fill="none"
                    stroke={padColor}
                    strokeWidth="1.5"
                    opacity="0.8"
                    strokeDasharray="2 2"
                  />
                )}
                <circle
                  cx="0"
                  cy="-22"
                  r="5.5"
                  fill={padColor}
                  opacity={contact_detected ? 1.0 : 0.45}
                  stroke="#687691"
                  strokeWidth="1.5"
                />
              </g>
            </g>
          </g>

          {/* MIDDLE FINGER (Digit 3) */}
          <g
            transform={`translate(205, 166) rotate(${middleCurl * 0.42})`}
            style={{ transition: 'transform 0.15s ease-out' }}
          >
            <circle cx="0" cy="0" r="10" fill="#2d3545" stroke="#687691" strokeWidth="2.5" />
            <circle cx="0" cy="0" r="4" fill="#181c24" />
            <rect x="-8.5" y="-46" width="17" height="46" rx="5" fill="#262d3a" stroke="#54627b" strokeWidth="2" />

            {/* Intermediate Phalanx */}
            <g
              transform={`translate(0, -46) rotate(${middleCurl * 0.52})`}
              style={{ transition: 'transform 0.15s ease-out' }}
            >
              <circle cx="0" cy="0" r="8" fill="#323c4d" stroke="#6d7b97" strokeWidth="2" />
              <rect x="-7.5" y="-38" width="15" height="38" rx="4" fill="#2b3342" stroke="#5d6c88" strokeWidth="2" />

              {/* Distal Phalanx + FSR */}
              <g
                transform={`translate(0, -38) rotate(${middleCurl * 0.52})`}
                style={{ transition: 'transform 0.15s ease-out' }}
              >
                <circle cx="0" cy="0" r="6.5" fill="#364052" stroke="#7584a2" strokeWidth="2" />
                <path d="M -6 0 L -5 -28 C -5 -34 5 -34 5 -28 L 6 0 Z" fill="#303848" stroke="#637391" strokeWidth="2" />
                {contact_detected && stateKey === 'POWER_GRIP' && (
                  <circle
                    cx="0"
                    cy="-23"
                    r="10"
                    fill="none"
                    stroke={padColor}
                    strokeWidth="1.5"
                    opacity="0.8"
                    strokeDasharray="2 2"
                  />
                )}
                <circle
                  cx="0"
                  cy="-23"
                  r="5.5"
                  fill={padColor}
                  opacity={contact_detected && stateKey === 'POWER_GRIP' ? 1.0 : 0.45}
                  stroke="#687691"
                  strokeWidth="1.5"
                />
              </g>
            </g>
          </g>

          {/* RING FINGER (Digit 4) */}
          <g
            transform={`translate(236, 170) rotate(${ringCurl * 0.42})`}
            style={{ transition: 'transform 0.15s ease-out' }}
          >
            <circle cx="0" cy="0" r="9.5" fill="#2d3545" stroke="#687691" strokeWidth="2.5" />
            <circle cx="0" cy="0" r="3.5" fill="#181c24" />
            <rect x="-8" y="-42" width="16" height="42" rx="5" fill="#262d3a" stroke="#54627b" strokeWidth="2" />

            {/* Intermediate Phalanx */}
            <g
              transform={`translate(0, -42) rotate(${ringCurl * 0.52})`}
              style={{ transition: 'transform 0.15s ease-out' }}
            >
              <circle cx="0" cy="0" r="7.5" fill="#323c4d" stroke="#6d7b97" strokeWidth="2" />
              <rect x="-7" y="-34" width="14" height="34" rx="4" fill="#2b3342" stroke="#5d6c88" strokeWidth="2" />

              {/* Distal Phalanx + FSR */}
              <g
                transform={`translate(0, -34) rotate(${ringCurl * 0.52})`}
                style={{ transition: 'transform 0.15s ease-out' }}
              >
                <circle cx="0" cy="0" r="6" fill="#364052" stroke="#7584a2" strokeWidth="2" />
                <path d="M -5.5 0 L -4.5 -25 C -4.5 -30 4.5 -30 4.5 -25 L 5.5 0 Z" fill="#303848" stroke="#637391" strokeWidth="2" />
                {contact_detected && stateKey === 'POWER_GRIP' && (
                  <circle
                    cx="0"
                    cy="-20"
                    r="9.5"
                    fill="none"
                    stroke={padColor}
                    strokeWidth="1.5"
                    opacity="0.8"
                    strokeDasharray="2 2"
                  />
                )}
                <circle
                  cx="0"
                  cy="-20"
                  r="5"
                  fill={padColor}
                  opacity={contact_detected && stateKey === 'POWER_GRIP' ? 1.0 : 0.45}
                  stroke="#687691"
                  strokeWidth="1.5"
                />
              </g>
            </g>
          </g>

          {/* PINKY FINGER (Digit 5) */}
          <g
            transform={`translate(264, 180) rotate(${pinkyCurl * 0.42})`}
            style={{ transition: 'transform 0.15s ease-out' }}
          >
            <circle cx="0" cy="0" r="8.5" fill="#2d3545" stroke="#687691" strokeWidth="2.5" />
            <circle cx="0" cy="0" r="3" fill="#181c24" />
            <rect x="-7" y="-34" width="14" height="34" rx="4" fill="#262d3a" stroke="#54627b" strokeWidth="2" />

            {/* Intermediate Phalanx */}
            <g
              transform={`translate(0, -34) rotate(${pinkyCurl * 0.52})`}
              style={{ transition: 'transform 0.15s ease-out' }}
            >
              <circle cx="0" cy="0" r="6.5" fill="#323c4d" stroke="#6d7b97" strokeWidth="2" />
              <rect x="-6" y="-28" width="12" height="28" rx="3.5" fill="#2b3342" stroke="#5d6c88" strokeWidth="2" />

              {/* Distal Phalanx + FSR */}
              <g
                transform={`translate(0, -28) rotate(${pinkyCurl * 0.52})`}
                style={{ transition: 'transform 0.15s ease-out' }}
              >
                <circle cx="0" cy="0" r="5" fill="#364052" stroke="#7584a2" strokeWidth="2" />
                <path d="M -4.5 0 L -4 -22 C -4 -27 4 -27 4 -22 L 4.5 0 Z" fill="#303848" stroke="#637391" strokeWidth="2" />
                {contact_detected && stateKey === 'POWER_GRIP' && (
                  <circle
                    cx="0"
                    cy="-17"
                    r="9"
                    fill="none"
                    stroke={padColor}
                    strokeWidth="1.5"
                    opacity="0.8"
                    strokeDasharray="2 2"
                  />
                )}
                <circle
                  cx="0"
                  cy="-17"
                  r="4.5"
                  fill={padColor}
                  opacity={contact_detected && stateKey === 'POWER_GRIP' ? 1.0 : 0.45}
                  stroke="#687691"
                  strokeWidth="1.5"
                />
              </g>
            </g>
          </g>

          {/* Slip Disturbance Alert Marker */}
          {slip_detected && (
            <g transform="translate(182, 140)">
              <rect x="-6" y="-12" width="68" height="24" rx="4" fill="#ef4444" opacity="0.95" />
              <text
                x="28"
                y="4"
                textAnchor="middle"
                fontSize="10"
                fontFamily="monospace"
                fontWeight="bold"
                fill="#ffffff"
                letterSpacing="1"
              >
                SLIP !
              </text>
            </g>
          )}
        </svg>
      </div>

      {/* Sensor Legend Footer */}
      <div className="w-full pt-2 border-t border-border-subtle flex items-center justify-between text-[11px] font-mono text-foreground-secondary">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5">
            <span
              className="w-2.5 h-2.5 rounded-full inline-block"
              style={{ backgroundColor: padColor }}
            />
            <span className="text-foreground">FSR Tactile Pad</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#687691] inline-block" />
            <span className="text-foreground-secondary">Servo Joint Pivot</span>
          </div>
        </div>
        <div className="text-foreground-secondary">
          Active Grip: <span className="text-foreground font-bold uppercase">{stateKey.replace('_', ' ')}</span>
        </div>
      </div>
    </div>
  );
};
