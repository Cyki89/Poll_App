import { useState } from "react";

const VotingQuestion = ({
  question = "What is your favorite color?",
  answers = [
    { id: 1, text: "answer1" },
    { id: 2, text: "answer2" },
    { id: 3, text: "answer3" },
  ],
  selectedList,
  onCheck = () => console.log("submited"),
}) => {
  const [selected, setSelected] = useState(() => {
    for (const answer of answers) {
      if (selectedList.includes(answer.id)) return answer.id;
    }
  });

  const onClick = (e) => {
    const currSelected = parseInt(e.target.dataset.id);
    onCheck(selected, currSelected);

    setSelected(currSelected);
  };

  return (
    <div className="voting-question">
      <h3 className="voting-txt">{question}</h3>
      <ul className="voting-answer-list">
        {answers.map((answer) => (
          <li
            key={answer.id}
            data-id={answer.id}
            className={
              answer.id === selected
                ? "voting-answer-item active"
                : "voting-answer-item"
            }
            onClick={onClick}>
            {answer.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VotingQuestion;
