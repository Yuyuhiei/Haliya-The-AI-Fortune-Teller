import React, { useEffect, useRef, useState } from 'react';
function Chat_test() {
  const [chatHistory, setChatHistory] = useState<{ sender: string, message: string }[]>([]);
  const [userMessage, setUserMessage] = useState('');
  var [userInDisp, setUserInDisp] = useState('')
  var [botOut, setBotOut] = useState('')
  var [mood, setMood] = useState('')
  var [greetingDone, setGreetingDone] = useState(false)

  const firstPrompt = async () => {
    // if (!greetingDone) {
      var resp = await fetch('http://127.0.0.1:5000/firstmsg')
      var data = await resp.json()
      return data.speakerMsg
    // }
  }
  async function handleFirstPrompt() {
    if (!greetingDone) {
      try{
        const firstMsg = await firstPrompt(); 
        console.log("firstmsg: " + firstMsg) 
        setBotOut(firstMsg) 
        console.log("botOut: "+botOut)
      } catch (error) {
        console.log('error')
      }
      setGreetingDone(true)
      return
    }
  }
 
  const prompt = async () => {
    const params = {
        method: 'POST',
        headers: {
            'Content-Type':'application/json' 
        },
        body: JSON.stringify({userMessage})
    }
    console.log(userMessage)
    await fetch('http://127.0.0.1:5000/prompt', params)
  }
  const response = async () => {
    var resp = await fetch('http://127.0.0.1:5000/response')
    var data = await resp.json()
    setBotOut(data.speakerMsg)
    setMood(data.mood)
  }

  const handleUserInput = async () => {
    // TODO: Make a request to the backend to get the bot's response
    setUserInDisp(userMessage)
    await prompt()
    await response()
  };
  const isMounted = useRef(true)


  useEffect(() => { //whenever we get a new output from Haliya, we'll append it to chat history
    console.log("first render:" +isMounted.current)
    if (!isMounted.current) {
      console.log('botout updated:' + botOut)
      setChatHistory([...chatHistory, { sender: 'haliya', message: botOut }])
    }
  },[botOut])
  useEffect(() => { //whenever we place userinput in userindisp, we append it to chat history 
    console.log("first render:" +isMounted.current)
    if (!isMounted.current) {
      console.log('userDisp updated: ' + userInDisp)
      setChatHistory([...chatHistory, { sender: 'user', message: userInDisp }])
    }
    setUserMessage('')
  },[userInDisp])


  useEffect(()=> {
    isMounted.current=false
  }, [])

  return (
    <div className='chat-container'>
      {chatHistory.map((chat, index) => (
        <p key={index}><b>{chat.sender}:</b> {chat.message}</p>
      ))}
      <input value={userMessage} onChange={e => setUserMessage(e.target.value)} />
      <button onClick={handleFirstPrompt}>Start</button>
      <button onClick={handleUserInput}>Send</button>
      <h1>{mood}</h1>
    </div>
  );
}

export default Chat_test;