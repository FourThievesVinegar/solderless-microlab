import React, { useState, useEffect } from 'react'
import { Dropdown, DropdownProps } from 'semantic-ui-react'

import { getLogs } from '../utils'

import './LogsPage.scss'

export function LogsPage() {
  const [logs, setLogs] = useState<false | { logs: string }>(false)
  const logLevels = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'DEBUG']
  const [selection, setSelection] = useState(logLevels)

  const selectionChanged = (_event: any, data: any) => {
    setSelection(data.value)
  }
  useEffect(() => {
    getLogs(setLogs)
  }, [])

  const filterLogs = (logString: string) => {
    return (
      logString
        // Get individual lines
        .split('\n')
        // Merge multi-line log messages into one string
        .reduce<string[]>((acc, next) => {
          // Strings that start YYYY-MM-DD are new log lines
          if (next.match(/^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])/)) {
            acc.push(next)

            // lines that do not start with a date either belong to the preceding
            // line as it's a multi-line message, or it's an empty string
            // from the extra \n on the last line which can be ignored.
          } else if (next !== '') {
            acc[acc.length - 1] += `\n${next}`
          }
          return acc
        }, [])
        // Filter for only selected log levels
        .filter(logLine => selection.some(level => logLine.includes(`[${level}]:`)))
        // put newest messages at the top of the screen
        .reverse()
        // back into one string
        .join('\n')
    )
  }

  return (
    <section className="page logs-page">
      <h4>Logs</h4>
      <Dropdown
        selection
        multiple={true}
        value={selection}
        options={logLevels.map(a => ({ key: a, text: a, value: a }))}
        onChange={selectionChanged}
      />
      <p>{logs && filterLogs(logs.logs)}</p>
    </section>
  )
}
