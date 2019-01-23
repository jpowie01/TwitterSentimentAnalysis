import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import * as React from 'react';
import { FormControl } from 'react-bootstrap';
import PieChart from 'react-minimal-pie-chart';
import { Sentiments, TweetCard } from 'src/tweet/tweet-card';
import { API_URL } from 'src/utils/ApiUtil';
import './search-form.css';

export class SearchForm extends React.Component<any, any> {
    public state: { value: string, tweets: any[], summary: any };

    constructor(props: {}, context: any) {
        super(props, context);

        this.onChange = this.onChange.bind(this);
        this.onBlur = this.onBlur.bind(this);

        this.state = {
            summary: [],
            tweets: [],
            value: ''
        };
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
                <div className='SearchForm-summary'>
                    <PieChart className='SearchForm-summary-chart' data={[
                        { title: Sentiments.POSITIVE, value: this.state.summary[Sentiments.POSITIVE], color: '#dff0d8' },
                        { title: Sentiments.NEUTRAL, value: this.state.summary[Sentiments.NEUTRAL], color: '#d9edf7' },
                        { title: Sentiments.NEGATIVE, value: this.state.summary[Sentiments.NEGATIVE], color: '#f2dede' },
                    ]}
                    />
                    <div className='SearchForm-summary-text'>
                    1. Lorem ipsum Lorem ipsum Lorem ipsum
                    1. Lorem ipsum Lorem ipsum Lorem ipsum
                    1. Lorem ipsum Lorem ipsum Lorem ipsum
                    1. Lorem ipsum Lorem ipsum Lorem ipsum
                    1. Lorem ipsum Lorem ipsum Lorem ipsum
                    </div>
                </div>
                <div className='SearchForm-cards'>
                    {this.state.tweets}
                </div>
            </div>
        );
    }

    private onChange(event: React.FormEvent<FormControl>): void {
        const element = event.target as HTMLInputElement;
        this.setState({
            value: element.value
        });
    }

    private async onBlur(): Promise<void> {
        const apiResponse: {newSummary: any, newTweets: any[]} = await this.getTweetsFromApi(this.state.value, 50);
        this.setState({
            summary: apiResponse.newSummary,
            tweets: apiResponse.newTweets
        });
    }

    private async getTweetsFromApi(query: string, size: number): Promise<{newSummary: any, newTweets: any[]}> {

        const config: AxiosRequestConfig = this.getSearchConfigParams(query, size);

        const TWEETS_API_URL = process.env.REACT_APP_REST_API_LOCATION + API_URL.TWEETS;

        this.setState({
            summary: {},
            tweets: []
        });

        const summary = {};
        summary[Sentiments.POSITIVE] = 0;
        summary[Sentiments.NEUTRAL] = 0;
        summary[Sentiments.NEGATIVE] = 0;

        const tweets: any[] = [];

        await axios.get(TWEETS_API_URL, config)
            .then((response: AxiosResponse) => {
                const tweetsBodies: any[] = response.data;

                tweetsBodies.forEach(tweet => {
                    const body = {
                        attentions: tweet.attention,
                        created: tweet.created,
                        fullname: tweet.fullname,
                        nickname: tweet.nickname,
                        photoUrl: tweet.photo_url,
                        sentiment: tweet.sentiment,
                        text: tweet.text,
                    };

                    summary[tweet.sentiment]++;

                    tweets.push(new TweetCard(body, this.context).render());
                });
            })
            .catch((error: any) => {
                alert(error.toString);
            });

        return {
            newSummary: summary,
            newTweets: tweets
        };
    }

    private getSearchConfigParams(query: string, size: number): AxiosRequestConfig {
        const searchParams = new URLSearchParams();
        searchParams.append('query', query);
        searchParams.append('size', size.toString());

        return {
            params: searchParams
        }
    }
}