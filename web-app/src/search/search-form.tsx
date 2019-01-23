import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import * as React from 'react';
import { FormControl } from 'react-bootstrap';
import { TweetCard } from 'src/tweet/tweet-card';
import { API_URL } from 'src/utils/ApiUtil';
import './search-form.css';

export class SearchForm extends React.Component<any, any> {
    public state: { value: string, tweets: any[] };

    constructor(props: {}, context: any) {
        super(props, context);

        this.onChange = this.onChange.bind(this);
        this.onBlur = this.onBlur.bind(this);

        this.state = {
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
        const newTweets = await this.getTweetsFromApi(this.state.value, 50);
        this.setState({
            tweets: newTweets
        })
    }

    private async getTweetsFromApi(query: string, size: number): Promise<any[]> {

        const config: AxiosRequestConfig = this.getSearchConfigParams(query, size);

        const TWEETS_API_URL = process.env.REACT_APP_REST_API_LOCATION + API_URL.TWEETS;

        this.setState({
            tweets: []
        });

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

                    tweets.push(new TweetCard(body, this.context).render());
                });
            })
            .catch((error: any) => {
                alert(error.toString);
            });

        return tweets;
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