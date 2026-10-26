import React from 'react';
import type { LogEntry } from '../types';

interface EventLogProps {
  logs: LogEntry[];
  onClear: () => void;
}

export const EventLog: React.FC<EventLogProps> = ({ logs, onClear }) => {
  const getCategoryStyle = (cat: LogEntry['category']) => {
    switch (cat) {
      case 'INFERENCE':
        return 'text-foreground font-semibold';
      case 'ADAPTIVE':
        return 'text-technical-amber';
      case 'TACTILE':
        return 'text-technical-green';
      case 'ACTUATION':
        return 'text-technical-blue';
      case 'SIGNAL':
        return 'text-foreground-secondary';
      case 'SYSTEM':
      default:
        return 'text-foreground-muted';
    }
  };

  return (
    <div className="bg-background-surface border border-border rounded-md p-4 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2 mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono uppercase tracking-wider text-foreground-secondary">
            System Event Log
          </span>
          <span className="text-[10px] bg-background-elevated border border-border px-1.5 py-0.5 rounded text-foreground-muted font-mono">
            {logs.length} entries
          </span>
        </div>
        <button
          onClick={onClear}
          className="text-[10px] font-mono text-foreground-muted hover:text-foreground uppercase tracking-wider underline transition-colors"
        >
          Clear Log
        </button>
      </div>

      {/* Log Feed */}
      <div className="flex-1 overflow-y-auto max-h-[160px] bg-background-subtle border border-border-subtle rounded p-2 font-mono text-xs space-y-1.5 select-text">
        {logs.length === 0 ? (
          <div className="text-foreground-muted text-center py-4 text-xs">
            No logged telemetry events.
          </div>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="flex items-start space-x-2 leading-relaxed">
              <span className="text-foreground-muted text-[11px] whitespace-nowrap">
                {log.timestamp}
              </span>
              <span
                className={`text-[10px] px-1 py-0.2 rounded border border-border-subtle bg-background-elevated whitespace-nowrap ${getCategoryStyle(
                  log.category
                )}`}
              >
                {log.category}
              </span>
              <span className="text-foreground text-[11px]">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
