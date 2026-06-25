import * as React from "react";
import { PRESETS, type Preset } from "./field-config";

/**
 * PresetPicker — load one of three illustrative research-style patterns. The
 * helper text makes clear these are not real people. Selecting one fills the
 * form and scores it through the same /predict path.
 */
export function PresetPicker({
  onSelect,
  disabled,
}: {
  onSelect: (preset: Preset) => void;
  disabled?: boolean;
}) {
  return (
    <div>
      <p className="text-sm font-medium text-ink">Or start from a preset pattern</p>
      <div className="mt-s3 flex flex-wrap gap-s2">
        {PRESETS.map((p) => (
          <button
            key={p.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(p)}
            className="min-h-[44px] rounded-sm border border-border bg-surface px-s4 text-sm text-ink transition-colors duration-fast hover:bg-subtle focus-visible:outline-focus disabled:opacity-50"
          >
            {p.label}
          </button>
        ))}
      </div>
      <p className="mt-s2 font-mono text-2xs text-muted">
        Presets are illustrative research-style patterns, not real people.
      </p>
    </div>
  );
}
