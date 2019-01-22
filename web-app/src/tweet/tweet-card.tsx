import * as React from 'react';
import { Panel } from 'react-bootstrap';
import './tweet-card.css';
import { WordAttentionPair } from './word-attention-pair';

export enum Sentiments {
    POSITIVE = "Positive",
    NEUTRAL = "Neutral",
    NEGATIVE = "Negative"
}

export class TweetCard extends React.Component<any, any> {
    public state: { textWithAttentions: WordAttentionPair[], textSentiment: Sentiments };

    constructor(props: { text: string, attentions: number[], sentiment: Sentiments }, context: any) {
        super(props, context);

        const preparedText: WordAttentionPair[] = this.prepareWordAttenitonPairs(props.text, props.attentions);

        this.state = {
            textSentiment: props.sentiment,
            textWithAttentions: preparedText
        }; // intentional
    }

    public render() {
        let tweetCardStyle: string = "";
        switch(this.state.textSentiment) {
            case Sentiments.POSITIVE: 
                tweetCardStyle = "success"
                break;
            case Sentiments.NEUTRAL:
                tweetCardStyle = "info"
                break;
            case Sentiments.NEGATIVE:
                tweetCardStyle = "danger"
                break;
        }

        return (
            <div className='TweetCard'>
                <Panel bsStyle={tweetCardStyle}>
                    <Panel.Heading>
                        <Panel.Title componentClass="h3">
                            {this.state.textSentiment}
                    </Panel.Title>
                    </Panel.Heading>
                    <Panel.Body>
                        <span>
                            {this.state.textWithAttentions.map((pair, i) => pair.render())}
                        </span>
                    </Panel.Body>
                </Panel>
            </div>
        );
    }

    private prepareWordAttenitonPairs(text: string, attentions: number[]): WordAttentionPair[] {
        const words: string[] = text.split(" ");
        const wordAttentionPairs: WordAttentionPair[] = [];

        words.forEach((value: string, index: number, array: string[]) => {
            wordAttentionPairs.push(new WordAttentionPair({word: value, attention: attentions[index]}, this.context));
        });

        return wordAttentionPairs;
    }
}