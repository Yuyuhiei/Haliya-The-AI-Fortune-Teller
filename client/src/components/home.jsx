import React, { useState } from 'react';
import ReactCardFlip from 'react-card-flip';
import { useSpring, animated } from 'react-spring';
import '../style/home.css';
import background from '../assets/bghome.gif';
import Haliya from '../assets/Haliya.png';
import Haliyanimated from '../assets/Haliya.gif';
import backCard from '../assets/cardback.png';
import frontCard1 from '../assets/front-cards/path_front.png';
import frontCard2 from '../assets/front-cards/grades_front.png';
import frontCard3 from '../assets/front-cards/physhealth_front.png';
import frontCard4 from '../assets/front-cards/lovelife_front.png';
import frontCard5 from '../assets/front-cards/profguesser_front.png';
import frontCard6 from '../assets/front-cards/decision_front.png';
import logo from '../assets/haliya_logo.png';

const BouncingDiv = ({children}) => {
  const bounce = useSpring({
    from: { transform: 'translate3d(0, 0px, 0)' },
    to: [
      { transform: 'translate3d(0, 10px, 0)' },
      { transform: 'translate3d(0, -10px, 0)' },
      { transform: 'translate3d(0, 0px, 0)' }
    ],
    config: { duration: 1000 },
    loop: true,
    reset: false
  });

  return <animated.div style={bounce}>{children}</animated.div>;
};

const HomePage = () => {
  const [flipped, setFlipped] = useState([false, false, false, false, false, false]);

  function flipCard(index) {
    setFlipped(flipped.map((flip, i) => i === index ? !flip : false));
  }

  const cards = [
    {
      img:frontCard1,
      cat:'life-path'
    },
    {
      img:frontCard2,
      cat:'grades'
    },
    {
      img:frontCard3,
      cat:'health'
    },
    {
      img:frontCard4,
      cat:'love'
    },
    {
      img:frontCard5,
      cat:'prof'
    },
    {
      img:frontCard6,
      cat:'decision'
    }

  ]

  const changeCategory = async (category) => {
    const params ={
      method: 'POST',
      headers: {
        'Content-Type':'application/json'
      },
      body: JSON.stringify({category})
    }
    await fetch('http://127.0.0.1:5000/set-category', params)
  }


  return (
    <div className="homepage">
      <img className="logo" src={logo} alt="logo" />
      <img className="background" src={background} alt="background" />
      <img className="character" src={Haliyanimated} alt="Haliya" />
      <div className="cards">
      {cards.map((card, index) => (
        <BouncingDiv>
          <div onMouseLeave={() => flipCard(index)}>
            <ReactCardFlip isFlipped={flipped[index]} flipDirection="horizontal" key={index}>
              <img
                className="card"
                src={backCard}
                alt="card back"
                onMouseEnter={() => flipCard(index)}
              />
              <a href='/chat/' onClick={()=>{changeCategory(card.cat)}}>
              <img
                className="card"
                src={card.img}
                alt="card front"
              />
              </a>
            </ReactCardFlip>
          </div>
        </BouncingDiv>
      ))}
      </div>
    </div>
  );
};

export default HomePage;