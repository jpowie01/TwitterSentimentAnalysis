import axios, { AxiosResponse } from 'axios';
import * as React from 'react';
import { Button, FormControl, FormGroup, Panel } from 'react-bootstrap';
import { Sentiments } from 'src/tweet/tweet-card';
import { WordAttentionPair } from 'src/tweet/word-attention-pair';
import { API_URL } from 'src/utils/ApiUtil';
import avatar from '../res/default_avatar.png';
import './input-card.css';

export class InputCard extends React.Component<any, any> {
    public state: {
        inputState: boolean,
        inputText: string,
        textWithAttentions: WordAttentionPair[],
        textSentiment: Sentiments
    };

    constructor(props: {}, context: any) {
        super(props, context);

        this.onCheckSentimentClick = this.onCheckSentimentClick.bind(this);
        this.onChangeTextClick = this.onChangeTextClick.bind(this);
        this.onInputChange = this.onInputChange.bind(this);

        this.state = {
            inputState: true,
            inputText: "",
            textSentiment: Sentiments.NONE,
            textWithAttentions: []
        };
    }

    public render() {
        return (
            <div className='TweetCard'>
                <Panel>
                    <Panel.Body>
                        <span className='TweetPredictedSentiment'>{this.state.textSentiment}</span>
                        <div className='TweetUserInfo'>
                            <img src={avatar} />
                            <div className='TweetUsernames'>
                                <span className='UserFullName'>You</span>
                                <span className='UserFullNick'>@YourNick</span>
                            </div>
                        </div>
                        {this.state.inputState
                            ? <form>
                                <FormGroup controlId="formControlsTextarea">
                                    <FormControl componentClass="textarea" onChange={this.onInputChange} value={this.state.inputText} placeholder="Your tweet" />
                                </FormGroup>
                                <Button bsStyle="info" onClick={this.onCheckSentimentClick}>Check sentiment</Button>
                            </form>
                            : <div>
                                <span className='TweetText'>
                                    {this.state.textWithAttentions.map((pair, i) => pair.render())}
                                </span>
                                <div className='Input-Card-button'>
                                    <Button bsStyle="primary" onClick={this.onChangeTextClick}>Change message</Button>
                                </div>
                            </div>}
                    </Panel.Body>
                </Panel>
            </div>
        );
    }

    private onInputChange(event: React.FormEvent<FormControl>): void {
        const element = event.target as HTMLInputElement;
        this.setState({
            inputText: element.value
        });
    }

    private async onCheckSentimentClick(event: React.FormEvent<FormControl>): Promise<void> {
        const apiResponse: { text: WordAttentionPair[], sentiment: Sentiments } = await this.getTweetAnalysis(this.state.inputText);
        this.setState({
            inputState: false,
            textSentiment: apiResponse.sentiment,
            textWithAttentions: apiResponse.text
        });
    }

    private async getTweetAnalysis(inputText: string): Promise<{ text: WordAttentionPair[], sentiment: Sentiments }> {
        const ANALYSIS_API_URL = process.env.REACT_APP_REST_API_LOCATION + API_URL.ANALYSE;

        const config = new URLSearchParams();
        config.append('content', inputText);

        let analizedText: WordAttentionPair[] = [];
        let analizedSentiment: Sentiments = Sentiments.NONE;

        await axios.get(ANALYSIS_API_URL, { params: config })
            .then((response: AxiosResponse) => {
                const analizedTweet: any = response.data[0];

                analizedText = WordAttentionPair.prepareWordAttentionPairs(analizedTweet.sentiment, analizedTweet.text, analizedTweet.attention, this.context);
                analizedSentiment = analizedTweet.sentiment;
            })
            .catch((error: any) => {
                alert(error);
            });

        return {
            sentiment: analizedSentiment,
            text: analizedText
        }
    }

    private async onChangeTextClick(event: React.FormEvent<FormControl>): Promise<void> {
        this.setState({
            inputState: true,
            textWithAttentions: []
        });
    }
}