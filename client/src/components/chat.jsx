import React, { useState, useRef, useEffect, useLayoutEffect, useSyncExternalStore } from 'react';
import '../style/chat.css'; 
import Raiden from '../assets/Raiden.png'
import sendBtn from '../assets/send-icon.png'
import haliyaIcon from '../assets/haliyaicon.png'
import logo from '../assets/haliya_logo.png'
import path from '../assets/button-icons/path.png'
import grades from '../assets/button-icons/grades.png'
import physicalHealth from '../assets/button-icons/physical-health.png'
import loveLife from '../assets/button-icons/love-life.png'
import professorGuesser from '../assets/button-icons/professor-guesser.png'
import decisionMaker from '../assets/button-icons/decision-maker.png'
import mic from '../assets/mic-icon.png'
import userIcon from '../assets/user-icons/user-icon.png'
import startIcon from '../assets/button-icons/start-icon.png'
import neut1 from '../assets/haliya-exp/neutral1.png'
import neut2 from '../assets/haliya-exp/neutral2.png'
import hap1 from '../assets/haliya-exp/happy1.png'
import hap2 from '../assets/haliya-exp/happy2.png'
import sad1 from '../assets/haliya-exp/frown1.png'
import sad2 from '../assets/haliya-exp/frown2.png'

const Chat = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [userInDisp, setUserInDisp] = useState('')
  const [botOut, setBotOut] = useState('')
  const [mood, setMood] = useState('Neutral')
  const [speaking, setSpeaking] = useState(false)
  const chatContainerRef = useRef(null);
  const [started, setStarted] = useState(false)
  const [activeCategory, setActiveCategory] = useState('life-path');
  const [profGuess, setProfGuess] = useState(false)
  const [rasaOut, setRasaOut] = useState(false)
  const [rasaQuesNo, setRasaQuesNo] = useState(0)
  const [rasaLast, setRasaLast] = useState(false)
  const [rasaResetPrompt, setRasaResetPrompt] = useState(false)
  const [isRecording, setIsRecording] = useState(false);
  const [doneRecording, setDoneRecording] = useState(false);
  const [showStartBtn, setShowStartBtn] = useState(true);

  
  const startOver = async () => {
    setShowStartBtn(true);
    setStarted(false);
    setRasaOut('');
    setRasaQuesNo(0);
    setRasaLast(false);
    setRasaResetPrompt(false);
    setMood('Neutral');
    setChatHistory([]);
    setUserMessage('');
    await fetch('http://127.0.0.1:5000/clear-chat')
  };
  
  

  const firstPrompt = async () => {
    // if (!greetingDone) {
      var resp = await fetch('http://127.0.0.1:5000/firstmsg')
      var data = await resp.json()
      return data.speakerMsg
    // }
  }
  async function handleFirstPrompt() {
    if (!started) {
      setShowStartBtn(false);
      try{
        setSpeaking(true)
        const firstMsg = await firstPrompt(); 
        console.log("firstmsg: " + firstMsg) 
        setBotOut(firstMsg) 
        setMood('Neutral')
        await fetch('http://127.0.0.1:5000/speech')
        setSpeaking(false)
        console.log("botOut: "+botOut)
      } catch (error) {
        console.log('error')
      }
      setStarted(true)
      return
    }
  }

  const changeCategory = async (category) => {
    setShowStartBtn(true)
    setStarted(false)
    setActiveCategory(category);
    if (category=='prof') {
      retryRasa()
      setProfGuess(true)
      const params ={
        method: 'POST',
        headers: {
          'Content-Type':'application/json'
        },
        body: JSON.stringify({category})
      }
      setChatHistory([])
      setUserMessage('')
      await fetch('http://127.0.0.1:5000/set-category', params)
      return
    }
    setProfGuess(false)
    const params ={
      method: 'POST',
      headers: {
        'Content-Type':'application/json'
      },
      body: JSON.stringify({category})
    }
    setChatHistory([])
    setUserMessage('')
    await fetch('http://127.0.0.1:5000/set-category', params)
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
    setSpeaking(true)
    var resp = await fetch('http://127.0.0.1:5000/response')
    var data = await resp.json()
    setBotOut(data.speakerMsg)
    setMood(data.mood)
    await fetch('http://127.0.0.1:5000/speech')
    setSpeaking(false)
  }

  const handleUserInput = async () => {
    if (userMessage==('')) {return}
    if (!started || speaking) {return}
    setUserInDisp(userMessage)
    await prompt()
    await response()
  };

  const fetchRasa = async (ans) => {
    if (speaking) {return}
    setMood('Neutral')
    var choice = [
      ['/affirm{"hair":"long"}', '/deny{"hair":"short"}', '/unknown{"hair":"unknown"}'],
      ['/affirm{"height":"tall"}', '/deny{"height":"ave"}', '/unknown{"height":"unknown"}'],
      ['/affirm{"glasses":"yes"}', '/deny{"glasses":"no"}', '/unknown{"glasses":"unknown"}'],
      ['/affirm{"position":"chairperson"}', '/deny{"position":"faculty"}', '/unknown{"position":"unknown"}'],
      ['/affirm{"year1":"true","year2":"false","year3":"false","year4":"false"}', '/deny{"year1":"false"}', '/unknown'],
      ['/affirm{"year1":"false","year2":"true","year3":"false","year4":"false"}', '/deny{"year2":"false"}', '/unknown'],
      ['/affirm{"year1":"false","year2":"false","year3":"true","year4":"false"}', '/deny{"year3":"false"}', '/unknown'],
      ['/affirm{"year1":"false","year2":"false","year3":"false","year4":"true"}', '/deny{"year4":"false"}', '/unknown'],
    ]
    if (rasaLast) {
      rasaResult(ans==0?true:false)
      return
    }
    if (rasaResetPrompt) {
      if (ans == 0) {
        retryRasa();
        startRasa();
      } else {
        retryRasa();
      }
    }
    var msg = choice[rasaQuesNo][ans]
    var params = {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'charset':'UTF-8',
      },
      body: JSON.stringify({'sender':'user', 'message':msg})
    }
    setSpeaking(true)
    var resp = await fetch('http://localhost:5005/webhooks/rest/webhook', params)
    var data = await resp.json()
    var msg = data[0]['text']
    setRasaQuesNo(rasaQuesNo+1)
    if (rasaQuesNo == 4) {setRasaLast(true)}
    console.log('rasa qusetion number: ' + rasaQuesNo)
    setRasaOut(msg)
    await fetch('http://127.0.0.1:5000/post-rasa', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg})})
    await fetch('http://127.0.0.1:5000/speech')
    setSpeaking(false)
  }
  
  const startRasa = async () => {
    setShowStartBtn(false);
    setRasaLast(false)
    setRasaResetPrompt(false)
    setMood('Neutral')
    var params = {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'charset':'UTF-8',
      },
      body: JSON.stringify({'sender':'user', 'message':'/start'})
    }
    setSpeaking(true)
    var resp = await fetch('http://localhost:5005/webhooks/rest/webhook', params)
    var data = await resp.json()
    var msg = data[0]['text']
    setRasaOut(msg)
    setStarted(true)
    console.log('rasa start msg: ' + msg)
    await fetch('http://127.0.0.1:5000/post-rasa', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg})})
    await fetch('http://127.0.0.1:5000/speech')
    setSpeaking(false)
  }

  const retryRasa = async () => {
    setRasaLast(false)
    setRasaResetPrompt(false)
    var params = {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'charset':'UTF-8',
      },
      body: JSON.stringify({'sender':'user', 'message':'/restart'})
    }
    await fetch('http://localhost:5005/webhooks/rest/webhook', params)
    setRasaOut('')
    setRasaQuesNo(0)
    setStarted(false)
  }

  const rasaResult = async (correct) => {
    var msg = correct ? 'Hehe. I knew it. Shall we go again?' : 'Awh. That\'s a shame. Care to give me another chance?'
    setMood(correct?'Happy':'Concerned')
    setRasaOut(msg)
    setSpeaking(true)
    await fetch('http://127.0.0.1:5000/post-rasa', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg})})
    await fetch('http://127.0.0.1:5000/speech')
    setSpeaking(false)
    setRasaResetPrompt(true)
    setRasaLast(false)
  }

  const startRecording = async () => {
    if (!started || speaking) {return}
    setIsRecording(true);
    const response = await fetch('http://127.0.0.1:5000/start_recording', { method: 'POST' });
    const data = await response.json();
    console.log(data.status);
  };

  const stopRecording = async () => {
    setIsRecording(false);
    const response = await fetch('http://127.0.0.1:5000/stop_recording', { method: 'POST' });
    const data = await response.json();
    console.log(data.status);
    setUserMessage(data.transcription); // Set the transcription result as userMessage
    setDoneRecording(true); // Process the transcription as if it were user input
  };

  const isMounted = useRef(true)

  useEffect(() => { //whenever we get a new output from Haliya, we'll append it to chat history
    console.log("first render:" +isMounted.current)
    if (!isMounted.current && botOut!='') {
      console.log('botout updated:' + botOut)
      setChatHistory([...chatHistory, { sender: 'haliya', msg: botOut }])
      setBotOut('')
    }
  },[botOut])
  useEffect(() => { //whenever we place userinput in userindisp, we append it to chat history 
    console.log("first render:" +isMounted.current)
    if (!isMounted.current) {
      console.log('userDisp updated: ' + userInDisp)
      setChatHistory([...chatHistory, { sender: 'user', msg: userInDisp }])
    }
    setUserMessage('')
  },[userInDisp])
  useEffect(()=> {
    if (!isMounted.current && doneRecording) {
      handleUserInput()
      setDoneRecording(false)
    }
  }, [doneRecording])

  useLayoutEffect(() => {
    // Scroll to the bottom of the chat container whenever a new message is added
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  useEffect(()=> {
    isMounted.current=false
  }, [])

  useEffect(()=> {
    async function getCatgeory() {
      var resp = await fetch('http://127.0.0.1:5000/get-category')
      var data = await resp.json()
      changeCategory(data.category)    
    }
    getCatgeory()
  }, [])
  // TODO:
  // ADD BACKEND FUNCTIONALITIES (DONE (mostly): HARLEY)
  // ADD MORE FUNCTIONALITIES

  return (
    <div className='ChatInterface'>
      <div className="sideBar">
        <div className="upperSide">
          <div className="upperSideTop">
            <img src={logo} alt="" />
          </div>
            <div className="upperSideBottom">
              <button className={`midBtn ${activeCategory === 'life-path' ? 'active' : ''}`} onClick={() => {changeCategory('life-path')}}><img src={path} alt="" className="button-icons"/>PATH</button>
              <button className={`midBtn ${activeCategory === 'grades' ? 'active' : ''}`} onClick={() => {changeCategory('grades')}}><img src={grades} alt="" className="button-icons"/>GRADES</button>
              <button className={`midBtn ${activeCategory === 'love' ? 'active' : ''}`} onClick={() => {changeCategory('love')}}><img src={loveLife} alt="" className="button-icons"/>LOVE LIFE</button>
              <button className={`midBtn ${activeCategory === 'health' ? 'active' : ''}`} onClick={() => {changeCategory('health')}}><img src={physicalHealth} alt="" className="button-icons"/>PHYSICAL HEALTH</button>
              <button className={`midBtn ${activeCategory === 'decision' ? 'active' : ''}`} onClick={() => {changeCategory('decision')}}><img src={decisionMaker} alt="" className="button-icons"/>DECISION MAKER</button>
              <button className={`midBtn ${activeCategory === 'prof' ? 'active' : ''}`} onClick={() => {changeCategory('prof')}}><img src={professorGuesser} alt="" className="button-icons"/>PROFESSOR GUESSER</button>
              <button className="startOverBtn" onClick={startOver}>🔄 Start Over</button>
            </div>
        </div>
      </div>

      {!profGuess && <div className="main">
         <div className="chats" ref={chatContainerRef}>
          {showStartBtn && <button className="startButton" onClick={handleFirstPrompt}><img src={startIcon} alt="" className="start-icon"/>START</button>}
          {chatHistory.map((chatItem, index) => {
            var clssNme = chatItem.sender=='haliya' ? 'chat bot' : 'chat'
            return(
              <div className={clssNme} key={index}>
                <img className='chatImg' src={chatItem.sender=='haliya' ? haliyaIcon : userIcon} alt="" /> <p className='txt'>{chatItem.msg}</p>
              </div>
            )
          }
          )}
          {/* expressions */}
          {mood=='Neutral' && speaking && <img id='haliya-half' src={neut2}/>}
          {mood=='Neutral' && !speaking && <img id='haliya-half' src={neut1}/>}
          {mood=='Happy' && speaking && <img id='haliya-half' src={hap2}/>}
          {mood=='Happy' && !speaking && <img id='haliya-half' src={hap1}/>}
          {mood=='Concerned' && speaking && <img id='haliya-half' src={sad2}/>}
          {mood=='Concerned' && !speaking && <img id='haliya-half' src={sad1}/>}
         </div>
         <div className="chatFooter">
             <div className="inp">
                 {/* <input type="text" placeholder='Message Haliya' value={userMessage} onChange={e => setUserMessage(e.target.value)}/> */}
                 <input 
                  type="text" 
                  placeholder = {started?'Talk to Haliya':'Click start...'} 
                  value={userMessage} 
                  onChange={e => setUserMessage(e.target.value)}
                  onKeyPress={e => {
                    if (e.key === 'Enter') {
                      handleUserInput();
                      e.preventDefault(); // Prevents the addition of a new line in the input when pressing Enter
                    }
                  }}
                  disabled={!started}
                />
                  {isRecording && <p className='active-mic'>Haliya is listening ...</p>}
                  <button 
                  className="mic" 
                  onClick={isRecording ? stopRecording : startRecording}
                  style={isRecording ? {
                    filter: 'drop-shadow(0 0 2px rgba(79, 2, 95, 0.5)) drop-shadow(0 0 2px rgba(79, 2, 95, 0.5)) drop-shadow(0 0 2px rgba(79, 2, 95, 0.5)) drop-shadow(0 0 2px rgba(79, 2, 95, 0.5))',
                    transition: '0.5s ease-in-out'
                  } : {}}
                >
                  <img src={mic} className="mic" alt=""/>
                </button>
                 <button className="send">
                     <img src={sendBtn} onClick={handleUserInput} alt=""/>
                 </button>
             </div>
             <p>Haliya is for fun only.</p>
         </div>
      </div>} 
      
      {profGuess && <div className="main">
        {!(rasaOut == '') && <div className="chat bot">
          <p className='txt'>{rasaOut}</p>
        </div>}
        {started && <div className="rasa-buttons">
          <button className="rasaButtons green-button" onClick={() => {
            fetchRasa(0)
          }
          }><span>Yes</span><i></i></button>
          <button className="rasaButtons red-button" onClick={() => {
            fetchRasa(1)
          }
          }><span>No</span><i></i></button>
          {/*{!rasaLast && !rasaResetPrompt && <button className="rasaButtons grey-button" onClick={() => {
            fetchRasa(2)
          }
          }><span>I don't know</span><i></i></button>}*/}
        </div>}
        <p className='tooltip'>Note: In this section, Haliya will ONLY guess a Computer Science professor's name</p>
        {/* expressions */}
        {mood == 'Neutral' && speaking && <img id='haliya-half' src={neut2}/>}
        {mood == 'Neutral' && !speaking && <img id='haliya-half' src={neut1}/>}
        {mood == 'Happy' && speaking && <img id='haliya-half' src={hap2}/>}
        {mood == 'Happy' && !speaking && <img id='haliya-half' src={hap1}/>}
        {mood == 'Concerned' && speaking && <img id='haliya-half' src={sad2}/>}
        {mood == 'Concerned' && !speaking && <img id='haliya-half' src={sad1}/>}
        {showStartBtn && <div className="rasa-buttons">
          <button className="startButton" onClick={startRasa}><img src={startIcon} alt="" className="start-icon"/>START
          </button>
        </div>}
      </div>}

    </div>
  );
}

export default Chat;