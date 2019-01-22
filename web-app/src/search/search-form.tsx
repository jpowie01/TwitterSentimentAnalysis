import * as React from 'react';
import { FormControl } from 'react-bootstrap';
import { Sentiments, TweetCard } from 'src/tweet/tweet-card';
import './search-form.css';

export class SearchForm extends React.Component<any, any> {
    public state: { value: string, tweets: any[] };

    constructor(props: {}, context: any) {
        super(props, context);

        this.onChange = this.onChange.bind(this);

        this.state = {
            tweets: [],
            value: ''
        }

        const tweetPositive = new TweetCard({ text: "I like trains", attentions: [0.12, 0.60, 0.2], sentiment: Sentiments.POSITIVE }, context).render();
        const tweetNeutral = new TweetCard({ text: "Trains", attentions: [0.01], sentiment: Sentiments.NEUTRAL }, context).render();
        const tweetNegative = new TweetCard({ text: "I hate trains", attentions: [0.12, 0.60, 0.2], sentiment: Sentiments.NEGATIVE }, context).render();
        this.state.tweets.push(tweetPositive);
        this.state.tweets.push(tweetNeutral);
        this.state.tweets.push(tweetPositive);
        this.state.tweets.push(tweetNegative);
        this.state.tweets.push(tweetNegative);
    }

    public render() {
        return (
            <div className='SearchForm'>
                <form className='SearchForm-input'>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="Enter phrase, username or hashtag"
                        onChange={this.onChange}
                        onBlur={this.onBlur} />
                </form>
                <div className='SearchForm-cards'>
                    {this.state.tweets}
                </div>
            </div>
        );
    }

    private onBlur(): void {
        // alert('Blur');
    }

    private onChange(event: React.FormEvent<FormControl>): void {
        const element = event.target as HTMLInputElement;
        this.setState({
            value: element.value
        });
    }
}