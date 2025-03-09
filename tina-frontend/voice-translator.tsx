"use client"

import { useState } from "react"
import { Mic, History } from "lucide-react"
import { motion } from "framer-motion"

export default function VoiceTranslator() {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)

  const toggleRecording = () => {
    setIsRecording(!isRecording)
    if (!isRecording) {
      setRecordingTime(0)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-slate-50 to-blue-50">
      <div className="flex flex-col items-center space-y-8">
        {/* Recording visualization */}
        <div className="relative w-32 h-32 flex items-center justify-center">
          {/* Ripple effects */}
          {isRecording && (
            <>
              <motion.div
                className="absolute w-full h-full rounded-full bg-blue-100"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.3, 0, 0.3],
                }}
                transition={{
                  duration: 2,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "easeInOut",
                }}
              />
              <motion.div
                className="absolute w-full h-full rounded-full bg-blue-100"
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.2, 0, 0.2],
                }}
                transition={{
                  duration: 2,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "easeInOut",
                  delay: 0.5,
                }}
              />
            </>
          )}

          {/* Main microphone button */}
          <motion.button
            onClick={toggleRecording}
            className="relative z-10 w-20 h-20 rounded-full bg-black text-white shadow-lg focus:outline-none hover:bg-gray-800 transition-colors"
            whileTap={{ scale: 0.95 }}
          >
            <Mic className="w-8 h-8 mx-auto" />
          </motion.button>
        </div>

        {/* Timer */}
        {isRecording && (
          <div className="text-gray-600 font-mono">
            {String(Math.floor(recordingTime / 60)).padStart(2, "0")}:{String(recordingTime % 60).padStart(2, "0")}
          </div>
        )}

        {/* Recording control button */}
        <button
          onClick={toggleRecording}
          className={`px-6 py-2 rounded-full transition-all ${
            isRecording ? "bg-red-50 text-red-500 hover:bg-red-100" : "bg-blue-50 text-blue-500 hover:bg-blue-100"
          }`}
        >
          {isRecording ? "Stop Recording" : "Start Recording"}
        </button>

        {/* History button */}
        <button className="flex items-center gap-2 text-gray-400 hover:text-gray-600 transition-colors">
          <History className="w-5 h-5" />
          <span>Browse History</span>
        </button>
      </div>
    </div>
  )
}

