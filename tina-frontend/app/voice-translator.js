"use client"

import { useState, useEffect, useRef } from "react"
import { Mic, History, X } from "lucide-react"
import TranscribeFile from "../src/services/TranscribeService"
import ReactMarkdown from "react-markdown"

export const VoiceTranslator = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [timer, setTimer] = useState(0)
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)
  const [transcription, setTranscription] = useState("") // Samenvatting/HTML response
  const [summary, setSummary] = useState("")
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])

  useEffect(() => {
    let interval
    if (isRecording) {
      interval = setInterval(() => {
        setTimer((prevTimer) => prevTimer + 1)
      }, 1000)
    } else if (!isRecording && timer !== 0) {
      setTimer(0);
      clearInterval(interval);
    }
    return () => clearInterval(interval)
  }, [isRecording, timer])

  const startRecording = async () => {
    try {
      setTranscription("") // Clear previous transcription when starting a new recording
      setSummary("")

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorder.start()
      setIsRecording(true)
      console.log("Recording started")
    } catch (error) {
      console.error("Error accessing microphone:", error)
      alert("Unable to access microphone. Please check your permissions.")
    }
  }

  const stopRecording = async () => {
    if (!mediaRecorderRef.current) return

    return new Promise((resolve) => {
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: "audio/webm" })
        const audioUrl = URL.createObjectURL(audioBlob)
        console.log("Audio blob created:", audioBlob.size, "bytes")
        console.log("Audio URL:", audioUrl)

        // Create a File object from the Blob
        const audioFile = new File([audioBlob], "recording.webm", { type: "audio/webm" })
        console.log("Audio file created:", audioFile)

        const result = await TranscribeFile(audioFile)
        const transcribed = result?.transcription
        const summary = result?.summary
        console.log("Whisper API response:", transcribed)
        console.log("LLAMA API summary:", summary)

        setSummary(summary)
        setTranscription(transcribed)

        const newHistoryItem = {
          timestamp: new Date().toLocaleString(),
          duration: timer,
          transcription_summary: summary,
          transcription_response: transcribed, // Store the transcription in history
        }
        setHistory(prev => [...prev, newHistoryItem])

        // Clean up the media stream
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
        resolve()
      }

      mediaRecorderRef.current.stop()
    })
  }

  const toggleRecording = async () => {
    if (isRecording) {
      setIsRecording(false)
      await stopRecording()
      setTimer(0)
    } else {
      await startRecording()
    }
  }

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60)
    const seconds = time % 60
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
  }

  const playAudio = (audioUrl) => {
    const audio = new Audio(audioUrl)
    audio.play()
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-slate-50 to-blue-50 p-4 w-full">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">TINA</h1>
      <div className="relative w-32 h-32 flex items-center justify-center mb-4">
        {isRecording && (
          <div
            className="absolute w-full h-full rounded-full bg-blue-100 animate-ping opacity-75"
            style={{
              animation: "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
            }}
          />
        )}
        <button
          onClick={toggleRecording}
          className="relative z-10 w-20 h-20 flex items-center justify-center rounded-full bg-black text-white shadow-lg focus:outline-none hover:bg-gray-800 transition-colors duration-200"
          style={{
            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
          }}
        >
          <Mic size={32} />
        </button>
      </div>
      <div className="text-2xl font-mono mb-4 text-gray-700">{formatTime(timer)}</div>
      <button
        className={`mb-4 px-6 py-2 rounded-full transition-all duration-200 ${
          isRecording ? "bg-red-50 text-red-500 hover:bg-red-100" : "bg-blue-50 text-blue-500 hover:bg-blue-100"
        }`}
        onClick={toggleRecording}
      >
        {isRecording ? "Stop opname" : "Begin opname"}
      </button>
      <button
        className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors duration-200"
        onClick={() => setShowHistory(true)}
      >
        <History size={20} />
        <span>Bekijk gespreksverloop</span>
      </button>

      {/* Info Panel for Transcription & Summary */}
      {transcription && summary && (
        <div className="mt-6 w-full max-w-md">
          {/* Summary Card */}
          <div className="mb-4 bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-blue-600 px-4 py-3">
              <h2 className="text-lg font-semibold text-white">Samenvatting</h2>
            </div>
            <div className="p-4">
              <div className="prose prose-sm max-h-[200px] overflow-y-auto">
                <ReactMarkdown>{summary}</ReactMarkdown>
              </div>
            </div>
          </div>

          {/* Full Transcription Card */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-gray-700 px-4 py-3">
              <h2 className="text-lg font-semibold text-white">Volledige transcriptie</h2>
            </div>
            <div className="p-4">
              <div className="prose prose-sm max-h-[300px] overflow-y-auto">
                <ReactMarkdown>{transcription}</ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      )}

      {showHistory && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Gespreksverloop</h2>
              <button onClick={() => setShowHistory(false)} className="text-gray-500 hover:text-gray-700">
                <X size={24} />
              </button>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {history.length === 0 ? (
                <p className="text-gray-500 text-center py-4">Geen opnamehistorie beschikbaar</p>
              ) : (
                history.map((item, index) => (
                  <div key={index} className="mb-4 p-3 bg-gray-100 rounded">
                    <p className="text-sm text-gray-600">{item.timestamp}</p>
                    <p className="font-medium">Duur: {formatTime(item.duration)}</p>
                    <p className="font-medium">Samenvatting:</p>
                    <section className="prose">
                        <ReactMarkdown>{`"${item.transcription_summary}"`}</ReactMarkdown>
                    </section>
                    <p className="font-medium">Volledige transcriptie:</p>
                    <section className="prose">
                        <ReactMarkdown>{`"${item.transcription_response}"`}</ReactMarkdown>
                    </section>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
