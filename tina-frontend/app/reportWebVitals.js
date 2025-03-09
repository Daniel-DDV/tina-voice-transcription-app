// src/reportWebVitals.js
import { reportWebVitals as originalWebVitals } from "react-dom/client"

export default function reportWebVitals(onPerfEntry) {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    originalWebVitals(onPerfEntry)
  }
}

